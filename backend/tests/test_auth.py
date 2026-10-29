"""Tests of login and logout (app/api/auth.py).

To be decided: the login mode (username and password, or sample profiles).
"""


def test_login_with_valid_credentials_returns_token():
    """POST /api/auth/login with the right password returns a session token."""
    raise NotImplementedError


def test_login_with_wrong_password_is_refused():
    """A wrong password returns an error and no token."""
    raise NotImplementedError


def test_user_locked_after_several_failures():
    """After several failed attempts, even the right password is refused for a while."""
    raise NotImplementedError


def test_logout_revokes_token():
    """After POST /api/auth/logout, the token is refused by the API and the MCP server."""
    raise NotImplementedError
