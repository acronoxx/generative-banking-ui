"""FastAPI application of the backend: single entry point to the banking data.

Run from the backend folder: uvicorn app.main:app --port 8000

Two parts are mounted, both calling the same services (app/services/):
- /api: HTTP routes used by the page (login, transfer confirmation) and by the tests;
- /mcp: MCP server exposing the agent tools (app/mcp/server.py), streamable HTTP transport.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api import accounts, advisors, auth, products, transactions, transfers
from app.mcp.server import mcp


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Start and stop the MCP session manager with the application.

    A FastMCP app mounted in FastAPI does not run its own lifespan.
    """
    async with mcp.session_manager.run():
        yield


def create_app() -> FastAPI:
    """Create the backend application: routers under /api, MCP server under /mcp."""
    app = FastAPI(lifespan=lifespan)
    # The page (Vite, port 5173) calls /api directly: login and transfer confirmation
    app.add_middleware(
        CORSMiddleware, allow_origins=["http://localhost:5173"], allow_methods=["*"], allow_headers=["*"]
    )

    for module in (auth, accounts, transactions, transfers, products, advisors):
        app.include_router(module.router, prefix="/api")

    # Errors raised by the services and app/security.py, turned into HTTP statuses
    for error, status in ((PermissionError, 401), (LookupError, 404), (ValueError, 400)):
        app.add_exception_handler(error, _error_handler(status))

    app.mount("/mcp", mcp.streamable_http_app())
    return app


def _error_handler(status: int):
    async def handler(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse({"detail": str(exc)}, status_code=status)

    return handler


app = create_app()
