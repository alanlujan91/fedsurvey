"""Data models for SCF survey data."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, NonNegativeInt

from .config import FIRST_YEAR, LAST_YEAR


class SCFRecord(BaseModel):
    """Represents a single SCF survey record.

    Attributes
    ----------
        year: Survey year
        income: Total household income
        wealth: Net worth
        weight: Survey weight
        age: Age of household head
        education: Education level
        marital_status: Marital status

    """

    year: int = Field(..., ge=FIRST_YEAR, le=LAST_YEAR)
    income: float = Field(..., ge=0)
    wealth: float
    weight: float = Field(..., gt=0)
    age: int | None = Field(None, ge=0, le=120)
    education: str | None
    marital_status: str | None


class SCFMetadata(BaseModel):
    """Metadata for SCF datasets."""

    year: int = Field(..., ge=FIRST_YEAR, le=LAST_YEAR)
    file_type: str = Field(..., pattern="^(stata|sas|csv)$")
    processed_date: datetime = Field(default_factory=datetime.now)
    record_count: NonNegativeInt = Field(default=0)
