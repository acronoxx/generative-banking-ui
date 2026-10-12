from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .accounts import Account
    from .categories import Category
    from .cards import Card
from datetime import date , datetime
from decimal import Decimal
from sqlalchemy import String , Date , DateTime ,ForeignKey , Numeric
from sqlalchemy.orm import Mapped , mapped_column , relationship

from .base import Base
class BankTransaction(Base):
    __tablename__="transactions"
    id:Mapped[int]=mapped_column(primary_key=True)
    type:Mapped[str]=mapped_column(String(100))
    amount:Mapped[Decimal]=mapped_column(Numeric(15,2),nullable=False)
    currency:Mapped[str]=mapped_column(String(3),nullable=False,default="EUR")
    description:Mapped[str | None]=mapped_column(String(255),nullable=True)
    merchant:Mapped[str | None]=mapped_column(String(100))
    reference:Mapped[str | None]=mapped_column(String(100))
    transaction_date:Mapped[datetime]=mapped_column(DateTime(timezone=True))
    booked_at:Mapped[datetime]=mapped_column(DateTime(timezone=True))
    status:Mapped[str]=mapped_column(String(20),nullable=False,default="completed")
    account_id:Mapped[int]=mapped_column(ForeignKey("accounts.id"),nullable=False)
    account:Mapped["Account"]=relationship("Account",back_populates="transactions")
    category_id:Mapped[int | None]=mapped_column(ForeignKey("categories.id"),nullable=True)
    category:Mapped["Category | None"]=relationship("Category",back_populates="transactions")
    card_id:Mapped[int | None]=mapped_column(ForeignKey("cards.id"),nullable=True)
    card:Mapped["Card | None"]=relationship("Card",back_populates="transactions")