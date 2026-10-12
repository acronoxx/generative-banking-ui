
from sqlalchemy.orm import configure_mappers

from backend.models import (
    Account,
    Advisor,
    BankingProduct,
    Card,
    Category,
    Customer,
    Subscription,
    User,
)

configure_mappers()

print("Tous les modèles ont été chargés.")
print("Les relations SQLAlchemy sont correctement configurées.")
