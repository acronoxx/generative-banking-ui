"""Tests of the two-step transfer: prepared by the agent, confirmed by the customer on the page."""

import json
from decimal import Decimal

from conftest import call_mcp

from app.services import transfers
from database import FakeDB


def _prepare(client, token) -> int:
    """Prepare a transfer of 100 EUR from account 1, as the agent would through the MCP tool."""
    arguments = {"source_account_id": 1, "beneficiary_id": 1, "amount": "100", "reason": "test"}
    result = call_mcp(client, "tools/call", {"name": "prepare_transfer", "arguments": arguments}, token)
    return json.loads(result["content"][0]["text"])["id"]


def _balance(client, token) -> str:
    accounts = client.get("/api/accounts", headers={"Authorization": f"Bearer {token}"}).json()
    return next(a["balance"] for a in accounts if a["id"] == 1)


def test_prepare_transfer_moves_no_money():
    db = FakeDB()
    transfers.prepare_transfer(db, db.users[0], 1, 1, Decimal(100), "test")
    assert db.accounts[0].balance == Decimal("1250.40")


def test_confirm_moves_money(client, token):
    simulation_id = _prepare(client, token)
    response = client.post(
        f"/api/transfers/{simulation_id}/confirm",
        json={"password": "demo"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.json()["status"] == "confirmed"
    assert _balance(client, token) == "1150.40"


def test_confirm_with_wrong_password_is_refused(client, token):
    simulation_id = _prepare(client, token)
    response = client.post(
        f"/api/transfers/{simulation_id}/confirm", json={"password": "x"}, headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 401


def test_cancelled_simulation_cannot_be_confirmed(client, token):
    simulation_id = _prepare(client, token)
    headers = {"Authorization": f"Bearer {token}"}
    client.post(f"/api/transfers/{simulation_id}/cancel", headers=headers)
    response = client.post(f"/api/transfers/{simulation_id}/confirm", json={"password": "demo"}, headers=headers)
    assert response.status_code == 400
