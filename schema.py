from datetime import datetime

from pydantic import BaseModel


class AirRecord(BaseModel):
    """Record schema for db."""

    timestamp: datetime
    co2: int
    temperature: float
