"""Beneficiaries and transfers of the connected customer.

A transfer goes through two steps: the agent prepares it (pending simulation),
then the customer confirms it on the page with their password. Only the second
step, which never goes through the agent, moves money.
"""

from decimal import Decimal

from sqlalchemy.orm import Session

from app.schemas.transfers import BeneficiaryOut, TransferSimulationOut
from models import User


def list_beneficiaries(db: Session, user: User) -> list[BeneficiaryOut]:
    """Return the beneficiaries registered by the customer."""
    raise NotImplementedError


def prepare_transfer(
    db: Session, user: User, source_account_id: int, beneficiary_id: int, amount: Decimal, reason: str
) -> TransferSimulationOut:
    """Create a pending transfer simulation and return its summary.

    Checks that the source account and the beneficiary belong to the customer and
    that the amount is positive. Nothing is debited.
    """
    raise NotImplementedError


def confirm_transfer(db: Session, user: User, simulation_id: int) -> TransferSimulationOut:
    """Execute a pending simulation of the customer and mark it as confirmed.

    The password, if the login uses one (to be decided), has already been checked
    by the route (app/api/transfers.py).
    Raises an error if the simulation does not belong to the customer or is no longer pending.
    """
    raise NotImplementedError


def cancel_transfer(db: Session, user: User, simulation_id: int) -> TransferSimulationOut:
    """Mark a pending simulation of the customer as cancelled."""
    raise NotImplementedError
