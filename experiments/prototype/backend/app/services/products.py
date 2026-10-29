"""Banking products offered by the bank (same catalog for every customer)."""

from app.schemas.products import ProductOut
from database import FakeDB
from models import User


def list_products(db: FakeDB, user: User, product_type: str | None = None) -> list[ProductOut]:
    """Return the active products, optionally of one type."""
    return [ProductOut(**vars(p)) for p in db.products if product_type is None or p.product_type == product_type]


def get_product_details(db: FakeDB, user: User, product_id: int) -> ProductOut:
    """Return one active product. Raises an error if it does not exist."""
    for p in db.products:
        if p.id == product_id:
            return ProductOut(**vars(p))
    raise LookupError(f"Product {product_id} not found")
