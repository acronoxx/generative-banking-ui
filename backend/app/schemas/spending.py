"""Formats of the spending analysis (data of the SpendingChart component)."""

from decimal import Decimal

from pydantic import BaseModel


class CategorySpending(BaseModel):
    """Total spending of one category over a period."""

    category: str
    total: Decimal


class SpendingComparison(BaseModel):
    """Spending of one category over two periods, and their difference (second - first)."""

    category: str
    first_total: Decimal
    second_total: Decimal
    difference: Decimal
