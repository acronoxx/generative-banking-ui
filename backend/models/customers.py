from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .accounts import Account
    from .advisors import Advisor
from datetime import date

from sqlalchemy import Date, String,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Customer(Base):
    __tablename__ = "customers"

    # Identifiant
    id: Mapped[int] = mapped_column(primary_key=True)

    # Informations personnelles
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    date_of_birth: Mapped[date | None] = mapped_column(Date, nullable=True)

    # Adresse
    address: Mapped[str | None] = mapped_column(String(255), nullable=True)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    postal_code: Mapped[str | None] = mapped_column(String(20), nullable=True)
    country: Mapped[str] = mapped_column(
        String(100),
        default="France",
    )

    # Statut du client
    status: Mapped[str] = mapped_column(
        String(20),
        default="active",
    )
    advisor_id: Mapped[int | None] = mapped_column(
    ForeignKey("advisors.id"),
    nullable=True)

    # Relations avec les autres modèles
    #list parce qu'on veut dire que chaque client peut avoir plusieurs comptes
    #backpopulates indique une relation bidirectionelle
    accounts: Mapped[list["Account"]] = relationship(
        back_populates="customer"
    )
    advisor: Mapped["Advisor | None"] = relationship(
    back_populates="customers")

