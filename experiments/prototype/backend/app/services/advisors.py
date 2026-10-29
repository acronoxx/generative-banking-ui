"""Advisor of the connected customer and appointment slots."""

from datetime import datetime, time, timedelta

from app.schemas.advisors import AdvisorOut, AppointmentSlot
from database import FakeDB
from models import User


def get_advisor(db: FakeDB, user: User) -> AdvisorOut:
    """Return the advisor assigned to the customer (a single advisor in the prototype)."""
    return AdvisorOut(**vars(db.advisor))


def get_appointment_slots(db: FakeDB, user: User, reason: str) -> list[AppointmentSlot]:
    """Return simulated appointment slots with the customer's advisor.

    The database has no calendar: the slots are generated, nothing is booked.
    """
    tomorrow = datetime.combine(datetime.now().date() + timedelta(days=1), time(10))
    starts = [tomorrow, tomorrow + timedelta(hours=4), tomorrow + timedelta(days=1)]
    return [AppointmentSlot(start=s, end=s + timedelta(minutes=30)) for s in starts]
