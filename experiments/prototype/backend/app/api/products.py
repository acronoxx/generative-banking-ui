"""Read-only access to the banking products, same services as the list_products and get_product_details tools."""

from fastapi import APIRouter

from app.dependencies import CurrentUser, Db
from app.schemas.products import ProductOut
from app.services import products

router = APIRouter(prefix="/products", tags=["products"])


@router.get("")
def list_products(db: Db, user: CurrentUser, product_type: str | None = None) -> list[ProductOut]:
    """Return the available products, optionally of one type."""
    return products.list_products(db, user, product_type)


@router.get("/{product_id}")
def get_product_details(product_id: int, db: Db, user: CurrentUser) -> ProductOut:
    """Return one product."""
    return products.get_product_details(db, user, product_id)
