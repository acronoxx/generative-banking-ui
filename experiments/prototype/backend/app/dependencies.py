"""FastAPI dependencies of the HTTP routes: database session and connected user.

Routes declare them as parameter types: def route(db: Db, user: CurrentUser).
"""

from typing import Annotated

from fastapi import Depends, Header

from app import security
from database import FakeDB, SessionLocal
from models import User


def get_db() -> FakeDB:
    return SessionLocal()


Db = Annotated[FakeDB, Depends(get_db)]


def get_current_user(db: Db, authorization: Annotated[str | None, Header()] = None) -> User:
    """User of the Authorization header; PermissionError becomes a 401 (handler in app/main.py)."""
    return security.user_from_header(db, authorization)


CurrentUser = Annotated[User, Depends(get_current_user)]
