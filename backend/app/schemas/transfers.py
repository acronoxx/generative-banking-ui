"""Formats of the beneficiaries and transfers (data of the TransferConfirmation component)."""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class BeneficiaryOut(BaseModel):
    """A beneficiary registered by the customer."""

    id: int
    name: str
    masked_iban: str


class TransferSimulationOut(BaseModel):
    """Summary of a transfer simulation. status: pending, confirmed or cancelled."""

    id: int
    source_account_id: int
    beneficiary_name: str
    amount: Decimal
    currency: str
    reason: str
    status: str
    created_at: datetime
    confirmed_at: datetime | None


class TransferConfirmIn(BaseModel):
    """Password typed again by the customer in TransferConfirmation.

    To be decided: only needed if the login uses a password.
    """

    password: str
