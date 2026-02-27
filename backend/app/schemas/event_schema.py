from pydantic import BaseModel, Field
from datetime import datetime

class EventCreate(BaseModel):
    category: str = Field(..., examples=["transport", "electricity", "spending"])
    description: str = Field(..., examples=["Car trip to college"])
    value: float = Field(..., ge=0, examples=[12.5])
    co2_kg: float = Field(..., ge=0, examples=[2.4])

class EventOut(BaseModel):
    id: int
    category: str
    description: str
    value: float
    co2_kg: float
    created_at: datetime

    class Config:
        from_attributes = True