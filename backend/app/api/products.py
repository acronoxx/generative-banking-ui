"""Read-only access to the banking products, same services as the list_products and get_product_details tools."""

from fastapi import APIRouter

from app.schemas.products import ProductOut

router = APIRouter(prefix="/products", tags=["products"])


@router.get("")
def list_products(product_type: str | None = None) -> list[ProductOut]:
    """Return the available products, optionally of one type."""
    raise NotImplementedError


@router.get("/{product_id}")
def get_product_details(product_id: int) -> ProductOut:
    """Return one product."""
    raise NotImplementedError
