"""Prototype stand-in for backend/models/: plain dataclasses instead of SQLAlchemy models.

Only the fields used by the services are kept.
"""

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal


@dataclass
class User:
    id: int
    username: str
    password: str  # the real project stores a hash, never the password
    customer_id: int


@dataclass
class Account:
    id: int
    customer_id: int
    account_type: str
    iban: str
    balance: Decimal
    currency: str = "EUR"


@dataclass
class Transaction:
    id: int
    account_id: int
    transaction_date: datetime
    description: str
    merchant: str | None
    category: str
    amount: Decimal  # negative for a spending
    currency: str = "EUR"


@dataclass
class Beneficiary:
    id: int
    customer_id: int
    name: str
    iban: str


@dataclass
class TransferSimulation:
    id: int
    customer_id: int
    source_account_id: int
    beneficiary_id: int
    amount: Decimal
    reason: str
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.now)
    confirmed_at: datetime | None = None


@dataclass
class Product:
    id: int
    name: str
    product_type: str
    description: str
    monthly_fee: Decimal


@dataclass
class Advisor:
    id: int
    name: str
    email: str
    phone: str
    specialisation: str | None
