"""Shared fixtures: a fresh in-memory database and a test client for each test."""

import json

import pytest
from fastapi.testclient import TestClient

import database
from app.main import create_app
from app.mcp.server import mcp


@pytest.fixture
def client():
    database._db = database.FakeDB()
    # The MCP session manager can only run once: let streamable_http_app() create a new one
    mcp._session_manager = None
    # "with" runs the lifespan (MCP session manager); the MCP server only accepts a "localhost:<port>" Host header
    with TestClient(create_app(), base_url="http://localhost:8000") as client:
        yield client


@pytest.fixture
def token(client) -> str:
    return client.post("/api/auth/login", json={"username": "demo", "password": "demo"}).json()["token"]


def call_mcp(client: TestClient, method: str, params: dict, token: str | None = None) -> dict:
    """Send one JSON-RPC request to the MCP server and return its "result" (stateless: no initialize)."""
    headers = {"Accept": "application/json, text/event-stream"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    response = client.post(
        "/mcp/", json={"jsonrpc": "2.0", "id": 1, "method": method, "params": params}, headers=headers
    )
    data_line = next(line for line in response.text.splitlines() if line.startswith("data:"))
    return json.loads(data_line.removeprefix("data:"))["result"]
