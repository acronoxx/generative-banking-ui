import hashlib
import hmac
from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from models import User, AuditLog
from models import UserSession

def verify_pin(pin: str, stored_hash: str) -> bool:
    try:
        algorithm, iterations, salt, expected_hash = stored_hash.split("$")

        if algorithm != "pbkdf2_sha256":
            return False

        computed_hash = hashlib.pbkdf2_hmac(
            "sha256",
            pin.encode(),
            salt.encode(),
            int(iterations),
        )

        return hmac.compare_digest(
            computed_hash,
            bytes.fromhex(expected_hash),
        )

    except (ValueError, TypeError, AttributeError, OverflowError):
        return False

def authenticate_user(
    db: Session,
    username: str,
    password: str
) -> User | None:

    now = datetime.now(timezone.utc)

    # Verrouiller la ligne pour éviter les tentatives concurrentes
    user = db.scalar(
        select(User)
        .where(User.username == username)
        .with_for_update()
    )

    if user is None:
        db.add(AuditLog(
            user_id=None,
            event_type="login_failed",
            description="Unknown username",
            created_at=now
        ))
        db.commit()
        return None

    # Vérifier le verrouillage temporaire
    locked_until = user.app_pin_locked_until

    if locked_until is not None:
        # Le modèle utilise DateTime sans timezone
        if locked_until > now.replace(tzinfo=None):
            return None

    # Vérifier le PIN
    if not verify_pin(password, user.app_pin_hash):

        user.app_pin_failed_attempts = (
            user.app_pin_failed_attempts or 0
        ) + 1

        db.add(AuditLog(
            user_id=user.id,
            event_type="login_failed",
            description="Invalid PIN",
            created_at=now
        ))

        if user.app_pin_failed_attempts >= 5:
            user.app_pin_locked_until = (
                now + timedelta(minutes=15)
            ).replace(tzinfo=None)

            db.add(AuditLog(
                user_id=user.id,
                event_type="account_locked",
                description="Too many failed PIN attempts",
                created_at=now
            ))

        db.commit()
        return None

    # Vérifier le statut : adapter aux valeurs du dataset
    if user.status != "active":
        return None

    # Réinitialiser les tentatives après succès
    user.app_pin_failed_attempts = 0
    user.app_pin_locked_until = None

    db.add(AuditLog(
        user_id=user.id,
        event_type="login_success",
        description="Successful authentication",
        created_at=now
    ))

    db.commit()
    return user

def create_session(db: Session, user: User) -> str:
    """Create a session and return its secret token."""

    # 1. Generate a cryptographically secure random token
    token = secrets.token_urlsafe(32)

    # 2. Store only its SHA-256 hash
    token_hash = hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()

    # 3. Define session lifetime
    now = datetime.now(timezone.utc)

    session = UserSession(
        user_id=user.id,
        token_hash=token_hash,
        created_at=now,
        expires_at=now + timedelta(hours=2),
        revoked_at=None,
    )

    # 4. Save session in PostgreSQL
    db.add(session)
    db.commit()

    return token