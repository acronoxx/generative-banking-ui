"""Login and logout, called directly by the page.

Prototype: a single user (demo / demo), no lock after failures, no audit log.
"""

from typing import Annotated

from fastapi import APIRouter, Header

from app import security
from app.dependencies import Db
from app.schemas.auth import LoginIn, LoginOut

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(credentials: LoginIn, db: Db) -> LoginOut:
    """Check the username and password and return a new session token."""
    user = security.check_credentials(db, credentials.username, credentials.password)
    return LoginOut(token=security.create_token(db, user))


@router.post("/logout")
def logout(db: Db, authorization: Annotated[str | None, Header()] = None) -> None:
    """Revoke the session token of the request."""
    security.revoke_token(db, security.token_from_header(authorization))
