"""Spending analysis of the connected customer, computed from the transactions."""

from datetime import date

from sqlalchemy.orm import Session

from app.schemas.spending import CategorySpending, SpendingComparison
from models import User


def get_spending_by_category(db: Session, user: User, start_date: date, end_date: date) -> list[CategorySpending]:
    """Return the total spending per category over the period, all accounts of the customer together."""
    raise NotImplementedError


def compare_spending(
    db: Session, user: User, first_start: date, first_end: date, second_start: date, second_end: date
) -> list[SpendingComparison]:
    """Return, for each category, the spending of both periods and their difference."""
    raise NotImplementedError
