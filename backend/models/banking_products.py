
from typing import TYPE_CHECKING

from sqlalchemy import String, Text , Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .subscriptions import Subscription


class BankingProduct(Base):
    __tablename__ = "banking_products"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    product_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    monthly_fee: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    status: Mapped[str] = mapped_column(
        String(20),
        default="active",
        nullable=False,
    )

    subscriptions: Mapped[list["Subscription"]] = relationship(
        back_populates="product"
    )
