"""Beneficiaries and transfers of the connected customer.

A transfer goes through two steps: the agent prepares it (pending simulation),
then the customer confirms it on the page with their password. Only the second
step, which never goes through the agent, moves money.
"""

from datetime import datetime
from decimal import Decimal

from app.schemas.transfers import BeneficiaryOut, TransferSimulationOut
from app.services.accounts import mask_iban, own_account
from database import FakeDB
from models import Beneficiary, TransferSimulation, User


def _own_beneficiary(db: FakeDB, user: User, beneficiary_id: int) -> Beneficiary:
    for b in db.beneficiaries:
        if b.id == beneficiary_id and b.customer_id == user.customer_id:
            return b
    raise LookupError(f"Beneficiary {beneficiary_id} not found")


def _own_pending_simulation(db: FakeDB, user: User, simulation_id: int) -> TransferSimulation:
    for s in db.simulations:
        if s.id == simulation_id and s.customer_id == user.customer_id:
            if s.status != "pending":
                raise ValueError(f"Transfer {simulation_id} is already {s.status}")
            return s
    raise LookupError(f"Transfer {simulation_id} not found")


def _summary(db: FakeDB, user: User, s: TransferSimulation) -> TransferSimulationOut:
    return TransferSimulationOut(
        id=s.id,
        source_account_id=s.source_account_id,
        beneficiary_name=_own_beneficiary(db, user, s.beneficiary_id).name,
        amount=s.amount,
        currency="EUR",
        reason=s.reason,
        status=s.status,
        created_at=s.created_at,
        confirmed_at=s.confirmed_at,
    )


def list_beneficiaries(db: FakeDB, user: User) -> list[BeneficiaryOut]:
    """Return the beneficiaries registered by the customer."""
    return [
        BeneficiaryOut(id=b.id, name=b.name, masked_iban=mask_iban(b.iban))
        for b in db.beneficiaries
        if b.customer_id == user.customer_id
    ]


def prepare_transfer(
    db: FakeDB, user: User, source_account_id: int, beneficiary_id: int, amount: Decimal, reason: str
) -> TransferSimulationOut:
    """Create a pending transfer simulation and return its summary.

    Checks that the source account and the beneficiary belong to the customer and
    that the amount is positive. Nothing is debited.
    """
    own_account(db, user, source_account_id)
    _own_beneficiary(db, user, beneficiary_id)
    if amount <= 0:
        raise ValueError("The amount must be positive")
    simulation = TransferSimulation(
        id=len(db.simulations) + 1,
        customer_id=user.customer_id,
        source_account_id=source_account_id,
        beneficiary_id=beneficiary_id,
        amount=amount,
        reason=reason,
    )
    db.simulations.append(simulation)
    return _summary(db, user, simulation)


def confirm_transfer(db: FakeDB, user: User, simulation_id: int) -> TransferSimulationOut:
    """Execute a pending simulation of the customer and mark it as confirmed.

    The password has already been checked by the route (app/api/transfers.py).
    Raises an error if the simulation does not belong to the customer or is no longer pending.
    """
    simulation = _own_pending_simulation(db, user, simulation_id)
    account = own_account(db, user, simulation.source_account_id)
    if account.balance < simulation.amount:
        raise ValueError("Insufficient balance")
    account.balance -= simulation.amount
    simulation.status = "confirmed"
    simulation.confirmed_at = datetime.now()
    return _summary(db, user, simulation)


def cancel_transfer(db: FakeDB, user: User, simulation_id: int) -> TransferSimulationOut:
    """Mark a pending simulation of the customer as cancelled."""
    simulation = _own_pending_simulation(db, user, simulation_id)
    simulation.status = "cancelled"
    return _summary(db, user, simulation)
