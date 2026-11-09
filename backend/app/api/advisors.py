"""Read-only access to the advisor, same services as the get_advisor and get_appointment_slots tools."""

from fastapi import APIRouter

from app.schemas.advisors import AdvisorOut, AppointmentSlot

router = APIRouter(prefix="/advisor", tags=["advisors"])


@router.get("")
def get_advisor() -> AdvisorOut:
    """Return the advisor of the connected customer."""
    raise NotImplementedError


@router.get("/slots")
def get_appointment_slots(reason: str) -> list[AppointmentSlot]:
    """Return simulated appointment slots with the advisor."""
    raise NotImplementedError
