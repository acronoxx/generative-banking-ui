"""Format of a banking product (data of the ProductCard component)."""

from decimal import Decimal

from pydantic import BaseModel


class ProductOut(BaseModel):
    """A banking product offered by the bank."""

    id: int
    name: str
    product_type: str
    description: str | None
    monthly_fee: Decimal
