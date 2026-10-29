"""Spending analysis of the connected customer, computed from the transactions."""

from collections import defaultdict
from datetime import date
from decimal import Decimal

from app.schemas.spending import CategorySpending, SpendingComparison
from database import FakeDB
from models import User


def _totals(db: FakeDB, user: User, start_date: date, end_date: date) -> dict[str, Decimal]:
    account_ids = {a.id for a in db.accounts if a.customer_id == user.customer_id}
    totals: dict[str, Decimal] = defaultdict(Decimal)
    for t in db.transactions:
        if t.account_id in account_ids and t.amount < 0 and start_date <= t.transaction_date.date() <= end_date:
            totals[t.category] += -t.amount
    return totals


def get_spending_by_category(db: FakeDB, user: User, start_date: date, end_date: date) -> list[CategorySpending]:
    """Return the total spending per category over the period, all accounts of the customer together."""
    return [CategorySpending(category=c, total=t) for c, t in _totals(db, user, start_date, end_date).items()]


def compare_spending(
    db: FakeDB, user: User, first_start: date, first_end: date, second_start: date, second_end: date
) -> list[SpendingComparison]:
    """Return, for each category, the spending of both periods and their difference."""
    first = _totals(db, user, first_start, first_end)
    second = _totals(db, user, second_start, second_end)
    return [
        SpendingComparison(
            category=c,
            first_total=first.get(c, Decimal(0)),
            second_total=second.get(c, Decimal(0)),
            difference=second.get(c, Decimal(0)) - first.get(c, Decimal(0)),
        )
        for c in sorted(first.keys() | second.keys())
    ]
