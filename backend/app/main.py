"""FastAPI application of the backend: single entry point to the banking data.

Run from the backend folder: uvicorn app.main:app --port 8000

Two parts are mounted, both calling the same services (app/services/):
- /api: HTTP routes used by the page (login, transfer confirmation) and by the tests;
- /mcp: MCP server exposing the agent tools (app/mcp/server.py), streamable HTTP transport.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.api.auth import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Start and stop the MCP session manager with the application.

    A FastMCP app mounted in FastAPI does not run its own lifespan: the backend must run
    mcp.session_manager.run() around the application (async with ...: yield).
    """
    raise NotImplementedError

def create_app() -> FastAPI:
    """Create the backend application."""

    app = FastAPI(
        title="Generative Banking API",
        description="Backend API for our AI-native banking application",
        version="0.1.0"
    )
    app.include_router(auth_router, prefix="/api")
    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app


app = create_app()


