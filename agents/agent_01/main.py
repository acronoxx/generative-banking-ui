"""AG-UI server of the banking assistant, called by the CopilotKit runtime.

Run from this folder: python main.py (the backend must already be running).
"""

from fastapi import FastAPI, Request

import config
from tools import SESSION_TOKEN_KEY


def read_session_token(request: Request) -> str | None:
    """Return the Authorization header of the request ("Bearer <token>"), or None.

    The page sends it to the CopilotKit runtime, which forwards it to the agent by default.
    To be decided: whether a session token is used (depends on the login mode).
    """
    raise NotImplementedError


def create_app() -> FastAPI:
    """Create the AG-UI server.

    1. load the banking tools from the backend (tools.load_backend_tools), once;
    2. build the agent with them (agent.build_agent) and wrap it in a LangGraphAgent;
    3. declare our own AG-UI endpoint POST "/" (add_langgraph_fastapi_endpoint is not
       used: it drops the request headers, so the session token would be lost).

    At each request, the endpoint clones the LangGraphAgent, stores the session token
    in its run config (config["configurable"][SESSION_TOKEN_KEY]), runs it and streams
    its steps (text, tool calls, A2UI messages) as AG-UI events (EventEncoder).
    """
    raise NotImplementedError


if __name__ == "__main__":
    # uvicorn.run(create_app(), host="127.0.0.1", port=config.AGENT_PORT)
    raise NotImplementedError
