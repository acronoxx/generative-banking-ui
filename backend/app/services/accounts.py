"""Accounts and transactions of the connected customer."""

from sqlalchemy.orm import Session

from app.schemas.accounts import AccountOut
from app.schemas.transactions import TransactionOut
from models import User
from sqlalchemy import select
from models import Account

def list_accounts(db: Session, user: User) -> list[AccountOut]:
    """Return the accounts belonging to the authenticated customer."""

    if user.customer_id is None:
        return []

    statement = (
        select(Account)
        .where(Account.customer_id == user.customer_id)
        .order_by(Account.id)
    )

    accounts = db.scalars(statement).all()

    result = []

    for account in accounts:
        masked_iban = "****" + account.iban[-4:]

        account_out = AccountOut(
            id=account.id,
            account_type=account.account_type,
            masked_iban=masked_iban,
            balance=account.balance,
            currency=account.currency,
        )

        result.append(account_out)

    return result


def get_recent_transactions(db: Session, user: User, account_id: int, limit: int) -> list[TransactionOut]:
    """Return the last transactions of an account, most recent first.

    Raises an error if the account does not belong to the customer.
    """
    raise NotImplementedError
