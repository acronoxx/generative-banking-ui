"""Advisor of the connected customer and appointment slots."""

from sqlalchemy.orm import Session

from app.schemas.advisors import AdvisorOut, AppointmentSlot
from models import User


def get_advisor(db: Session, user: User) -> AdvisorOut:
    """Return the advisor assigned to the customer (customers.advisor_id)."""
    raise NotImplementedError


def get_appointment_slots(db: Session, user: User, reason: str) -> list[AppointmentSlot]:
    """Return simulated appointment slots with the customer's advisor.

    The database has no calendar: the slots are generated, nothing is booked.
    """
    raise NotImplementedError
