"""Login and logout, called directly by the page.

To be decided: the login mode (username and password, or sample profiles).
These routes are written for a username, a password and a session token.
"""


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.auth import LoginIn, LoginOut
from app.services.auth import authenticate_user, create_session

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginOut)
def login(
    credentials: LoginIn,
    db: Session = Depends(get_db)
) -> LoginOut:

    user = authenticate_user(
        db,
        credentials.username,
        credentials.password
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials or account unavailable"
        )

    token = create_session(db, user)

    return LoginOut(token=token)
