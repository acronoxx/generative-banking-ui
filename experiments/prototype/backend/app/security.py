"""Passwords and session tokens.

Prototype: plain-text password, tokens kept in memory, no expiry, no lock after failures.
"""

import secrets

from database import FakeDB
from models import User


def check_credentials(db: FakeDB, username: str, password: str) -> User:
    """Return the user if the username and password match. Raises PermissionError otherwise."""
    for user in db.users:
        if user.username == username and secrets.compare_digest(user.password, password):
            return user
    raise PermissionError("Wrong username or password")


def create_token(db: FakeDB, user: User) -> str:
    """Create a new session token for the user."""
    token = secrets.token_urlsafe(32)
    db.sessions[token] = user.id
    return token


def revoke_token(db: FakeDB, token: str) -> None:
    db.sessions.pop(token, None)


def token_from_header(authorization: str | None) -> str:
    """Extract the token from an Authorization header ("Bearer <token>"). Raises PermissionError."""
    if not authorization or not authorization.startswith("Bearer "):
        raise PermissionError("Missing session token")
    return authorization.removeprefix("Bearer ")


def user_from_header(db: FakeDB, authorization: str | None) -> User:
    """Return the user owning the session token of the header. Raises PermissionError if unknown."""
    user_id = db.sessions.get(token_from_header(authorization))
    if user_id is None:
        raise PermissionError("Invalid session token")
    return next(user for user in db.users if user.id == user_id)
