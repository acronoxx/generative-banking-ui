"""Prototype stand-in for backend/database.py: in-memory data of a single customer, no PostgreSQL.

SessionLocal() returns the same FakeDB object every time, where the real project returns
a SQLAlchemy session. Everything is lost when the backend restarts.
"""

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal

from models import Account, Advisor, Beneficiary, Product, Transaction, TransferSimulation, User


def _transaction(id: int, day: str, description: str, merchant: str | None, category: str, amount: str) -> Transaction:
    return Transaction(id, 1, datetime.fromisoformat(day), description, merchant, category, Decimal(amount))


@dataclass
class FakeDB:
    users: list[User] = field(default_factory=lambda: [User(1, "demo", "demo", customer_id=1)])
    accounts: list[Account] = field(
        default_factory=lambda: [
            Account(1, 1, "checking", "FR7630006000011234567890189", Decimal("1250.40")),
            Account(2, 1, "savings", "FR7630006000019876543210143", Decimal("8400.00")),
        ]
    )
    transactions: list[Transaction] = field(
        default_factory=lambda: [
            _transaction(1, "2026-09-03T12:30", "Lunch", "Le Bistrot", "restaurants", "-18.50"),
            _transaction(2, "2026-09-10T18:05", "Groceries", "Carrefour", "groceries", "-72.30"),
            _transaction(3, "2026-09-21T20:15", "Dinner", "Sushi Bar", "restaurants", "-42.00"),
            _transaction(4, "2026-09-28T09:00", "Salary", None, "income", "2300.00"),
            _transaction(5, "2026-10-02T13:00", "Lunch", "Le Bistrot", "restaurants", "-21.00"),
            _transaction(6, "2026-10-08T17:40", "Groceries", "Carrefour", "groceries", "-65.10"),
            _transaction(7, "2026-10-15T21:00", "Dinner", "Pizzeria Roma", "restaurants", "-35.80"),
            _transaction(8, "2026-10-20T08:10", "Train ticket", "SNCF", "transport", "-54.00"),
            _transaction(9, "2026-10-28T09:00", "Salary", None, "income", "2300.00"),
        ]
    )
    beneficiaries: list[Beneficiary] = field(
        default_factory=lambda: [
            Beneficiary(1, 1, "Marie Dupont", "FR7612345000010000000000123"),
            Beneficiary(2, 1, "Landlord", "FR7698765000010000000000456"),
        ]
    )
    simulations: list[TransferSimulation] = field(default_factory=list)
    products: list[Product] = field(
        default_factory=lambda: [
            Product(1, "Travel insurance", "insurance", "Medical costs and cancellation abroad.", Decimal("4.90")),
            Product(2, "Premium card", "card", "Higher limits and travel assistance.", Decimal("12.00")),
            Product(3, "Savings booklet", "savings", "Tax-free savings account.", Decimal("0.00")),
        ]
    )
    advisor: Advisor = field(
        default_factory=lambda: Advisor(1, "Paul Martin", "paul.martin@bank.example", "01 23 45 67 89", "savings")
    )
    # Session tokens: token -> user id (the real project stores them in a table)
    sessions: dict[str, int] = field(default_factory=dict)


_db = FakeDB()


def SessionLocal() -> FakeDB:
    return _db
