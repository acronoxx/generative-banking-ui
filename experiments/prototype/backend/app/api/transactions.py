"""Read-only access to the transactions, same service as the get_recent_transactions tool."""

from fastapi import APIRouter

from app.dependencies import CurrentUser, Db
from app.schemas.transactions import TransactionOut
from app.services import accounts

router = APIRouter(prefix="/accounts", tags=["transactions"])


@router.get("/{account_id}/transactions")
def get_recent_transactions(account_id: int, db: Db, user: CurrentUser, limit: int = 20) -> list[TransactionOut]:
    """Return the last transactions of an account of the connected customer."""
    return accounts.get_recent_transactions(db, user, account_id, limit)
