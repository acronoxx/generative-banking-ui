"""Confirmation and cancellation of a transfer, called directly by the page
(TransferConfirmation component), never by the agent.
"""

from fastapi import APIRouter

from app import security
from app.dependencies import CurrentUser, Db
from app.schemas.transfers import TransferConfirmIn, TransferSimulationOut
from app.services import transfers

router = APIRouter(prefix="/transfers", tags=["transfers"])


@router.post("/{simulation_id}/confirm")
def confirm(simulation_id: int, body: TransferConfirmIn, db: Db, user: CurrentUser) -> TransferSimulationOut:
    """Check the password again, then confirm the simulation (services.transfers.confirm_transfer)."""
    security.check_credentials(db, user.username, body.password)
    return transfers.confirm_transfer(db, user, simulation_id)


@router.post("/{simulation_id}/cancel")
def cancel(simulation_id: int, db: Db, user: CurrentUser) -> TransferSimulationOut:
    """Cancel the simulation (services.transfers.cancel_transfer)."""
    return transfers.cancel_transfer(db, user, simulation_id)
