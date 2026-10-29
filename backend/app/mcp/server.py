"""MCP server exposing the banking tools of the agent (mounted under /mcp by app/main.py).

Rules shared by all the tools:
- no tool takes a customer id: the customer is deduced from the session token that the
  agent sends in the Authorization header (agents/agent_01/tools.py);
- listing the tools needs no token (the agent loads them at startup, before any login);
  calling a tool needs a valid one;
- a tool never returns the token: its result goes to the model, the page and the traces.

Each tool only reads the token, finds the user, then calls a service of app/services/.

To be decided: the login mode (username and password, or sample profiles) and so
whether the user is identified by a session token.
"""

from datetime import date
from decimal import Decimal

from mcp.server.fastmcp import Context, FastMCP

# Stateless: each request carries its own token, no MCP session is kept between calls.
mcp = FastMCP("banking", stateless_http=True, streamable_http_path="/")


def current_user(ctx: Context):
    """Return the user owning the session token of the current tool call.

    The Authorization header ("Bearer <token>") is read from
    ctx.request_context.request.headers, then checked by app/security.py
    (token known, not expired, not revoked). Raises an error if the token is missing or invalid.
    To be decided: with sample profiles, the header would carry the chosen profile instead.
    """
    raise NotImplementedError


@mcp.tool()
def list_accounts(ctx: Context) -> list[dict]:
    """List the accounts of the customer, with their balance."""
    raise NotImplementedError


@mcp.tool()
def get_recent_transactions(account_id: int, limit: int, ctx: Context) -> list[dict]:
    """Return the most recent transactions of one account of the customer.

    Args:
        account_id: id of the account, as returned by list_accounts.
        limit: number of transactions to return.
    """
    raise NotImplementedError


@mcp.tool()
def get_spending_by_category(start_date: date, end_date: date, ctx: Context) -> list[dict]:
    """Return the total spending of the customer per category over a period."""
    raise NotImplementedError


@mcp.tool()
def compare_spending(
    first_start: date, first_end: date, second_start: date, second_end: date, ctx: Context
) -> list[dict]:
    """Compare the spending of the customer per category between two periods."""
    raise NotImplementedError


@mcp.tool()
def list_beneficiaries(ctx: Context) -> list[dict]:
    """List the beneficiaries registered by the customer (the only possible transfer recipients)."""
    raise NotImplementedError


@mcp.tool()
def prepare_transfer(
    source_account_id: int, beneficiary_id: int, amount: Decimal, reason: str, ctx: Context
) -> dict:
    """Prepare a transfer: create a pending simulation and return its summary.

    No money is moved: the transfer is confirmed by the customer on the page
    (TransferConfirmation component -> POST /api/transfers/{id}/confirm), never by the agent.
    """
    raise NotImplementedError


@mcp.tool()
def list_products(ctx: Context, product_type: str | None = None) -> list[dict]:
    """List the available banking products, optionally of one type."""
    raise NotImplementedError


@mcp.tool()
def get_product_details(product_id: int, ctx: Context) -> dict:
    """Return the description and the monthly fee of one product."""
    raise NotImplementedError


@mcp.tool()
def get_advisor(ctx: Context) -> dict:
    """Return the advisor assigned to the customer."""
    raise NotImplementedError


@mcp.tool()
def get_appointment_slots(reason: str, ctx: Context) -> list[dict]:
    """Return simulated appointment slots with the customer's advisor."""
    raise NotImplementedError
