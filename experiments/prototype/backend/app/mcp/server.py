"""MCP server exposing the banking tools of the agent (mounted under /mcp by app/main.py).

Rules shared by all the tools:
- no tool takes a customer id: the customer is deduced from the session token that the
  agent sends in the Authorization header (agents/agent_01/tools.py);
- listing the tools needs no token (the agent loads them at startup, before any login);
  calling a tool needs a valid one;
- a tool never returns the token: its result goes to the model, the page and the traces.

Each tool only reads the token, finds the user, then calls a service of app/services/.
"""

from datetime import date
from decimal import Decimal

from mcp.server.fastmcp import Context, FastMCP

from app import security
from app.services import accounts, advisors, products, spending, transfers
from database import SessionLocal
from models import User

# Stateless: each request carries its own token, no MCP session is kept between calls.
mcp = FastMCP("banking", stateless_http=True, streamable_http_path="/")


def current_user(ctx: Context) -> User:
    """Return the user owning the session token of the current tool call.

    Raises PermissionError if the token is missing or invalid: FastMCP turns it into
    a tool error, so the model only sees "Invalid session token".
    """
    return security.user_from_header(SessionLocal(), ctx.request_context.request.headers.get("authorization"))


def dump(results) -> list[dict]:
    return [r.model_dump(mode="json") for r in results]


@mcp.tool()
def list_accounts(ctx: Context) -> list[dict]:
    """List the accounts of the customer, with their balance."""
    return dump(accounts.list_accounts(SessionLocal(), current_user(ctx)))


@mcp.tool()
def get_recent_transactions(account_id: int, limit: int, ctx: Context) -> list[dict]:
    """Return the most recent transactions of one account of the customer.

    Args:
        account_id: id of the account, as returned by list_accounts.
        limit: number of transactions to return.
    """
    return dump(accounts.get_recent_transactions(SessionLocal(), current_user(ctx), account_id, limit))


@mcp.tool()
def get_spending_by_category(start_date: date, end_date: date, ctx: Context) -> list[dict]:
    """Return the total spending of the customer per category over a period."""
    return dump(spending.get_spending_by_category(SessionLocal(), current_user(ctx), start_date, end_date))


@mcp.tool()
def compare_spending(
    first_start: date, first_end: date, second_start: date, second_end: date, ctx: Context
) -> list[dict]:
    """Compare the spending of the customer per category between two periods."""
    return dump(
        spending.compare_spending(SessionLocal(), current_user(ctx), first_start, first_end, second_start, second_end)
    )


@mcp.tool()
def list_beneficiaries(ctx: Context) -> list[dict]:
    """List the beneficiaries registered by the customer (the only possible transfer recipients)."""
    return dump(transfers.list_beneficiaries(SessionLocal(), current_user(ctx)))


@mcp.tool()
def prepare_transfer(source_account_id: int, beneficiary_id: int, amount: Decimal, reason: str, ctx: Context) -> dict:
    """Prepare a transfer: create a pending simulation and return its summary.

    No money is moved: the transfer is confirmed by the customer on the page
    (TransferConfirmation component -> POST /api/transfers/{id}/confirm), never by the agent.
    """
    simulation = transfers.prepare_transfer(
        SessionLocal(), current_user(ctx), source_account_id, beneficiary_id, amount, reason
    )
    return simulation.model_dump(mode="json")


@mcp.tool()
def list_products(ctx: Context, product_type: str | None = None) -> list[dict]:
    """List the available banking products, optionally of one type (insurance, card, savings)."""
    return dump(products.list_products(SessionLocal(), current_user(ctx), product_type))


@mcp.tool()
def get_product_details(product_id: int, ctx: Context) -> dict:
    """Return the description and the monthly fee of one product."""
    return products.get_product_details(SessionLocal(), current_user(ctx), product_id).model_dump(mode="json")


@mcp.tool()
def get_advisor(ctx: Context) -> dict:
    """Return the advisor assigned to the customer."""
    return advisors.get_advisor(SessionLocal(), current_user(ctx)).model_dump(mode="json")


@mcp.tool()
def get_appointment_slots(reason: str, ctx: Context) -> list[dict]:
    """Return simulated appointment slots with the customer's advisor."""
    return dump(advisors.get_appointment_slots(SessionLocal(), current_user(ctx), reason))
