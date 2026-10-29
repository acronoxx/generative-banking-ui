"""Banking tools of the agent.

The tools are not defined here: they are declared by the backend MCP server
(backend/app/mcp/server.py), next to the data. This module only connects to it
and converts its tools into LangChain tools.
"""

from collections.abc import Awaitable, Callable

from langchain_core.tools import BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.interceptors import MCPToolCallRequest

import config

# Key of the run config where main.py stores the user's session token for the tools.
# The run config is never sent to the model, nor to the page, nor to the traces.
SESSION_TOKEN_KEY = "auth_token"


async def add_session_token(request: MCPToolCallRequest, handler: Callable[[MCPToolCallRequest], Awaitable]):
    """MCP tool interceptor: add the user's session token to each tool call.

    The model never sees the token: it is not a tool argument.
    """
    token = request.runtime.config["configurable"].get(SESSION_TOKEN_KEY) if request.runtime else None
    if token:
        request = request.override(headers={**(request.headers or {}), "Authorization": token})
    return await handler(request)


async def load_backend_tools() -> list[BaseTool]:
    """Connect to the backend MCP server and return its tools (called once at startup, without any user)."""
    client = MultiServerMCPClient(
        {"backend": {"transport": "streamable_http", "url": config.BACKEND_MCP_URL}},
        tool_interceptors=[add_session_token],
    )
    return await client.get_tools()
