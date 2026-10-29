"""Tests of login and logout (app/api/auth.py)."""

from conftest import call_mcp


def test_login_with_valid_credentials_returns_token(token):
    """POST /api/auth/login with the right password returns a session token."""
    assert token


def test_login_with_wrong_password_is_refused(client):
    """A wrong password returns an error and no token."""
    response = client.post("/api/auth/login", json={"username": "demo", "password": "wrong"})
    assert response.status_code == 401
    assert "token" not in response.json()


def test_logout_revokes_token(client, token):
    """After POST /api/auth/logout, the token is refused by the API and the MCP server."""
    client.post("/api/auth/logout", headers={"Authorization": f"Bearer {token}"})
    assert client.get("/api/accounts", headers={"Authorization": f"Bearer {token}"}).status_code == 401
    assert call_mcp(client, "tools/call", {"name": "list_accounts", "arguments": {}}, token)["isError"]
