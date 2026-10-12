from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .customers import Customer
    from .cards import Card
    from .transactions import BankTransaction
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id"),
        nullable=False,
    )

    iban: Mapped[str] = mapped_column(
        String(34),
        unique=True,
        nullable=False,
    )

    account_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        default="EUR",
        nullable=False,
    )

    balance: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        default=Decimal("0.00"),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="active",
        nullable=False,
    )

    opened_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    customer: Mapped["Customer"] = relationship(back_populates="accounts")
    cards: Mapped[list["Card"]] = relationship(
        back_populates="account")
    transactions: Mapped[list["BankTransaction"]] = relationship(
        back_populates="account")
