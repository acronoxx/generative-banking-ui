"""Formats of the advisor and appointment slots (data of the AppointmentPicker component)."""

from datetime import datetime

from pydantic import BaseModel


class AdvisorOut(BaseModel):
    """The advisor assigned to the customer."""

    id: int
    name: str
    email: str
    phone: str
    specialisation: str | None


class AppointmentSlot(BaseModel):
    """A simulated appointment slot with the advisor."""

    start: datetime
    end: datetime
