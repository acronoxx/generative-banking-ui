"""Formats of the login route.

To be decided: the login mode (username and password, or sample profiles).
"""

from pydantic import BaseModel


class LoginIn(BaseModel):
    """Credentials typed by the user on the login page."""

    username: str
    password: str


class LoginOut(BaseModel):
    """Session token returned after a successful login, sent back in the Authorization header."""

    token: str
