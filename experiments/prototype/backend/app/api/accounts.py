"""Read-only access to the accounts, same service as the list_accounts tool (tests, classic screens)."""

from fastapi import APIRouter

from app.dependencies import CurrentUser, Db
from app.schemas.accounts import AccountOut
from app.services import accounts

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("")
def list_accounts(db: Db, user: CurrentUser) -> list[AccountOut]:
    """Return the accounts of the connected customer (services.accounts.list_accounts)."""
    return accounts.list_accounts(db, user)
