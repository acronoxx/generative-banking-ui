
from datetime import date, datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Date, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .accounts import Account
    from .subscriptions import Subscription
    from .transactions import BankTransaction


class Card(Base):
    __tablename__ = "cards"

    id: Mapped[int] = mapped_column(primary_key=True)

    account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id"),
        nullable=False,
    )

    subscription_id: Mapped[int | None] = mapped_column(
        ForeignKey("subscriptions.id"),
        nullable=True,
    )

    card_token: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    card_number_test: Mapped[str] = mapped_column(
        String(19),
        nullable=False,
    )

    last_four_digits: Mapped[str] = mapped_column(
        String(4),
        nullable=False,
    )

    expiry_month: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    expiry_year: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    card_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    physical_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    daily_payment_limit: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        nullable=False,
    )

    monthly_payment_limit: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        nullable=False,
    )

    daily_withdrawal_limit: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        nullable=False,
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        default="EUR",
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="active",
        nullable=False,
    )

    valid_from: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    expires_at: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    account: Mapped["Account"] = relationship(
        back_populates="cards"
    )

    subscription: Mapped["Subscription | None"] = relationship(
        back_populates="cards"
    )

    transactions: Mapped[list["BankTransaction"]] = relationship(
        back_populates="card"
    )
