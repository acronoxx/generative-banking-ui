from typing import TYPE_CHECKING
from sqlalchemy import CheckConstraint

if TYPE_CHECKING:
    from .customers import Customer
    from .advisors import Advisor
from datetime import date , datetime
from sqlalchemy import String , ForeignKey , Date , INT , DateTime
from sqlalchemy.orm import Mapped , mapped_column , relationship

from .base import Base
class User(Base):
    __tablename__="users"
    id:Mapped[int]=mapped_column(primary_key=True)
    username:Mapped[str]=mapped_column(String(100))
    app_pin_hash : Mapped[str] = mapped_column(String(255),nullable=False)
    app_pin_failed_attempts : Mapped[int]=mapped_column(INT ,default=0)
    app_pin_locked_until : Mapped[datetime|None]=mapped_column(DateTime,nullable=True)
    role : Mapped[str]=mapped_column(String(100),nullable=False)
    status : Mapped[str|None]=mapped_column(String(100),nullable=False)
    created_at : Mapped[date]=mapped_column(Date)
    
    customer_id : Mapped[int|None]= mapped_column(ForeignKey("customers.id"),nullable=True)
    advisor_id : Mapped[int|None]= mapped_column(ForeignKey("advisors.id"),nullable=True)
    
    #relations unidirectionelles car on ne veut pas associer un client a un user vue que le user peut aussi etre un advisor
    customer: Mapped["Customer | None"] = relationship()
    advisor: Mapped["Advisor | None"] = relationship()
    
    """Cette règle impose :
- customer : un profil client, aucun profil conseiller ;
- advisor : un profil conseiller, aucun profil client ;
- admin : aucun des deux profils."""
    
    __table_args__ = (
    CheckConstraint(
        """
        (role = 'customer' AND customer_id IS NOT NULL
         AND advisor_id IS NULL)
        OR
        (role = 'advisor' AND advisor_id IS NOT NULL
         AND customer_id IS NULL)
        OR
        (role = 'admin' AND customer_id IS NULL
         AND advisor_id IS NULL)
        """,
        name="user_role_profile_consistency",
    ),
)