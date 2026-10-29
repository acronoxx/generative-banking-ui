"""FastAPI application of the backend: single entry point to the banking data.

Run from the backend folder: uvicorn app.main:app --port 8000

Two parts are mounted, both calling the same services (app/services/):
- /api: HTTP routes used by the page (login, transfer confirmation) and by the tests;
- /mcp: MCP server exposing the agent tools (app/mcp/server.py), streamable HTTP transport.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Start and stop the MCP session manager with the application.

    A FastMCP app mounted in FastAPI does not run its own lifespan: the backend must run
    mcp.session_manager.run() around the application (async with ...: yield).
    """
    raise NotImplementedError


def create_app() -> FastAPI:
    """Create the backend application.

    1. include the routers of app/api/ under /api (auth, accounts, transactions,
       transfers, products, advisors);
    2. mount the MCP server under /mcp (app.mount("/mcp", mcp.streamable_http_app()),
       the server being declared with streamable_http_path="/").
    """
    raise NotImplementedError


# app = create_app()
