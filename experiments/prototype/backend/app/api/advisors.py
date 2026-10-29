"""Read-only access to the advisor, same services as the get_advisor and get_appointment_slots tools."""

from fastapi import APIRouter

from app.dependencies import CurrentUser, Db
from app.schemas.advisors import AdvisorOut, AppointmentSlot
from app.services import advisors

router = APIRouter(prefix="/advisor", tags=["advisors"])


@router.get("")
def get_advisor(db: Db, user: CurrentUser) -> AdvisorOut:
    """Return the advisor of the connected customer."""
    return advisors.get_advisor(db, user)


@router.get("/slots")
def get_appointment_slots(reason: str, db: Db, user: CurrentUser) -> list[AppointmentSlot]:
    """Return simulated appointment slots with the advisor."""
    return advisors.get_appointment_slots(db, user, reason)
