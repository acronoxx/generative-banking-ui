"""Tests of the MCP server rules (app/mcp/server.py)."""

from conftest import call_mcp


def test_tools_listed_without_token(client):
    """The agent lists the tools at startup, before any login: no token is needed."""
    tools = call_mcp(client, "tools/list", {})["tools"]
    assert "list_accounts" in {tool["name"] for tool in tools}


def test_tool_call_without_token_is_refused(client):
    """Calling a tool without an Authorization header returns an error, no data."""
    result = call_mcp(client, "tools/call", {"name": "list_accounts", "arguments": {}})
    assert result["isError"]


def test_tool_call_with_token_returns_data(client, token):
    result = call_mcp(client, "tools/call", {"name": "list_accounts", "arguments": {}}, token)
    assert not result["isError"]
    assert len(result["structuredContent"]["result"]) == 2


def test_tool_result_never_contains_token(client, token):
    """The token never appears in a tool result (sent to the model, the page and the traces)."""
    result = call_mcp(client, "tools/call", {"name": "list_accounts", "arguments": {}}, token)
    assert token not in str(result)
