"""Format of an account (data of the AccountCard component)."""

from decimal import Decimal

from pydantic import BaseModel


class AccountOut(BaseModel):
    """An account of the customer. The full IBAN is never returned."""

    id: int
    account_type: str
    masked_iban: str
    balance: Decimal
    currency: str
