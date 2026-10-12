
from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .customers import Customer
    from .banking_products import BankingProduct
    from .cards import Card


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True)

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id"),
        nullable=False,
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("banking_products.id"),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="active",
        nullable=False,
    )

    start_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    end_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    customer: Mapped["Customer"] = relationship()
    product: Mapped["BankingProduct"] = relationship(back_populates="subscriptions")

    cards: Mapped[list["Card"]] = relationship(
        back_populates="subscription"
    )
