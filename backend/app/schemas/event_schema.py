from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class EventCreate(BaseModel):
    category: str
    description: str
    value: float = Field(..., ge=0)

    transport_mode: Optional[str] = None
    spend_category: Optional[str] = "default"


class EventOut(BaseModel):
    id: int
    category: str
    description: str
    value: float
    co2_kg: float
    created_at: datetime

    class Config:
        from_attributes = True