"""Accounts and transactions of the connected customer."""

from sqlalchemy.orm import Session

from app.schemas.accounts import AccountOut
from app.schemas.transactions import TransactionOut
from models import User


def list_accounts(db: Session, user: User) -> list[AccountOut]:
    """Return the accounts of the customer (user.customer_id), with their balance and masked IBAN."""
    raise NotImplementedError


def get_recent_transactions(db: Session, user: User, account_id: int, limit: int) -> list[TransactionOut]:
    """Return the last transactions of an account, most recent first.

    Raises an error if the account does not belong to the customer.
    """
    raise NotImplementedError
