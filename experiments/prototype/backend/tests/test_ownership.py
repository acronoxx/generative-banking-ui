"""Tests of the ownership checks of app/services/: a customer only reaches their own data.

Prototype: a single customer, so "another customer's account" is an account that does not exist.
"""

from decimal import Decimal

import pytest

from app.services import accounts, transfers
from database import FakeDB


def test_list_accounts_returns_only_own_accounts():
    db = FakeDB()
    assert {a.id for a in accounts.list_accounts(db, db.users[0])} == {1, 2}


def test_transactions_of_other_customer_account_are_refused():
    db = FakeDB()
    with pytest.raises(LookupError):
        accounts.get_recent_transactions(db, db.users[0], account_id=99, limit=5)


def test_prepare_transfer_from_other_customer_account_is_refused():
    db = FakeDB()
    with pytest.raises(LookupError):
        transfers.prepare_transfer(db, db.users[0], 99, 1, Decimal(10), "test")
