from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from .db import Base

class FootprintEvent(Base):
    __tablename__ = "footprint_events"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, index=True)
    description = Column(String)
    value = Column(Float)
    co2_kg = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)