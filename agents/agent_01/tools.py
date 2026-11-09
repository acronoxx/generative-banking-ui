"""Banking tools of the agent.

The tools are not defined here: they are declared by the backend MCP server
(backend/app/mcp/server.py), next to the data. This module only connects to it
and converts its tools into LangChain tools.

To be decided: the login mode (username and password, or sample profiles) and so
whether a session token is used. The interceptor below is written for a token.
"""

from collections.abc import Awaitable, Callable

from langchain_core.tools import BaseTool
from langchain_mcp_adapters.interceptors import MCPToolCallRequest

import config

# Key of the run config where main.py stores the user's session token for the tools.
# The run config is never sent to the model, nor to the page, nor to the traces.
SESSION_TOKEN_KEY = "auth_token"


async def add_session_token(request: MCPToolCallRequest, handler: Callable[[MCPToolCallRequest], Awaitable]):
    """MCP tool interceptor: add the user's session token to each tool call.

    Reads the token stored by main.py in the run config
    (request.runtime.config["configurable"][SESSION_TOKEN_KEY]) and sends it to the
    backend in the Authorization header (request.override(headers=...)), then calls handler.
    The model never sees the token: it is not a tool argument.
    """
    raise NotImplementedError


async def load_backend_tools() -> list[BaseTool]:
    """Connect to the backend MCP server (streamable HTTP, config.BACKEND_MCP_URL) and return its tools.

    Called once at startup by main.py, without any user: the backend must be running
    and must allow listing the tools without a token (calling a tool requires one).
    The client is created with tool_interceptors=[add_session_token].
    """
    raise NotImplementedError
