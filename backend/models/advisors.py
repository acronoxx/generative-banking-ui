from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .customers import Customer 
from sqlalchemy import  String
from sqlalchemy.orm import Mapped , mapped_column , relationship

from .base import Base 

class Advisor(Base):
    __tablename__="advisors"
    id :Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column(String(100))
    email:Mapped[str]=mapped_column(String(255),unique=True,index=True)
    phone:Mapped[str]=mapped_column(String(30),unique=True)
    specialisation:Mapped[str|None]=mapped_column(String(100),nullable=True)
    status:Mapped[str]=mapped_column(String(100),default="active")
    customers:Mapped[list["Customer"]]=relationship(back_populates="advisor")