"""Login and logout, called directly by the page.

To be decided: the login mode (username and password, or sample profiles).
These routes are written for a username, a password and a session token.
"""

from fastapi import APIRouter

from app.schemas.auth import LoginIn, LoginOut

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(credentials: LoginIn) -> LoginOut:
    """Check the username and password and return a new session token.

    After several failures the user is temporarily locked. Every attempt is recorded in audit_logs.
    """
    raise NotImplementedError


@router.post("/logout")
def logout() -> None:
    """Revoke the session token of the request."""
    raise NotImplementedError
