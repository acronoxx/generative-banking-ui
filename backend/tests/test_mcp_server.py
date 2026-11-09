"""Tests of the MCP server rules (app/mcp/server.py)."""


def test_tools_listed_without_token():
    """The agent lists the tools at startup, before any login: no token is needed."""
    raise NotImplementedError


def test_tool_call_without_token_is_refused():
    """Calling a tool without an Authorization header returns an error, no data."""
    raise NotImplementedError


def test_tool_call_with_revoked_token_is_refused():
    """A token revoked by logout can no longer be used to call a tool.

    To be decided: only relevant if a session token is used.
    """
    raise NotImplementedError


def test_tool_result_never_contains_token():
    """The token never appears in a tool result (sent to the model, the page and the traces)."""
    raise NotImplementedError
