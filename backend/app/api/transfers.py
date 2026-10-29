"""Confirmation and cancellation of a transfer, called directly by the page
(TransferConfirmation component), never by the agent.
"""

from fastapi import APIRouter

from app.schemas.transfers import TransferConfirmIn, TransferSimulationOut

router = APIRouter(prefix="/transfers", tags=["transfers"])


@router.post("/{simulation_id}/confirm")
def confirm(simulation_id: int, body: TransferConfirmIn) -> TransferSimulationOut:
    """Check the password again, then confirm the simulation (services.transfers.confirm_transfer).

    To be decided: the password check only applies if the login uses a password.
    """
    raise NotImplementedError


@router.post("/{simulation_id}/cancel")
def cancel(simulation_id: int) -> TransferSimulationOut:
    """Cancel the simulation (services.transfers.cancel_transfer)."""
    raise NotImplementedError
