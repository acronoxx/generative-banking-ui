"""Accounts and transactions of the connected customer."""

from app.schemas.accounts import AccountOut
from app.schemas.transactions import TransactionOut
from database import FakeDB
from models import Account, User


def mask_iban(iban: str) -> str:
    return f"{iban[:4]} **** {iban[-4:]}"


def own_account(db: FakeDB, user: User, account_id: int) -> Account:
    """Return an account of the customer. Raises LookupError if it does not exist or is not theirs."""
    for account in db.accounts:
        if account.id == account_id and account.customer_id == user.customer_id:
            return account
    raise LookupError(f"Account {account_id} not found")


def list_accounts(db: FakeDB, user: User) -> list[AccountOut]:
    """Return the accounts of the customer (user.customer_id), with their balance and masked IBAN."""
    return [
        AccountOut(
            id=a.id, account_type=a.account_type, masked_iban=mask_iban(a.iban), balance=a.balance, currency=a.currency
        )
        for a in db.accounts
        if a.customer_id == user.customer_id
    ]


def get_recent_transactions(db: FakeDB, user: User, account_id: int, limit: int) -> list[TransactionOut]:
    """Return the last transactions of an account, most recent first.

    Raises an error if the account does not belong to the customer.
    """
    own_account(db, user, account_id)
    transactions = sorted(
        (t for t in db.transactions if t.account_id == account_id), key=lambda t: t.transaction_date, reverse=True
    )
    return [
        TransactionOut(
            id=t.id,
            transaction_date=t.transaction_date,
            description=t.description,
            merchant=t.merchant,
            category=t.category,
            amount=t.amount,
            currency=t.currency,
        )
        for t in transactions[:limit]
    ]
