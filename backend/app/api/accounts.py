"""Read-only access to the accounts, same service as the list_accounts tool (tests, classic screens)."""

from fastapi import APIRouter

from app.schemas.accounts import AccountOut

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("")
def list_accounts() -> list[AccountOut]:
    """Return the accounts of the connected customer (services.accounts.list_accounts)."""
    raise NotImplementedError
