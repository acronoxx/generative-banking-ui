"""Format of a transaction (one line of the TransactionList component)."""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class TransactionOut(BaseModel):
    """A transaction of an account of the customer."""

    id: int
    transaction_date: datetime
    description: str | None
    merchant: str | None
    category: str | None
    amount: Decimal
    currency: str
