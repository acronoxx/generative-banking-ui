"""Banking products offered by the bank (same catalog for every customer)."""

from sqlalchemy.orm import Session

from app.schemas.products import ProductOut
from models import User


def list_products(db: Session, user: User, product_type: str | None = None) -> list[ProductOut]:
    """Return the active products, optionally of one type."""
    raise NotImplementedError


def get_product_details(db: Session, user: User, product_id: int) -> ProductOut:
    """Return one active product. Raises an error if it does not exist."""
    raise NotImplementedError
