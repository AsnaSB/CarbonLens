from sqlalchemy import Column, Integer, Float, Date, DateTime
from datetime import datetime
from app.models.db import Base


class CreditLedger(Base):
    __tablename__ = "credit_ledger"

    id = Column(Integer, primary_key=True, index=True)

    # Week this summary represents (Monday start recommended)
    week_start_date = Column(Date, nullable=False)

    # Emissions comparison
    total_co2_week = Column(Float, nullable=False)
    total_co2_prev_week = Column(Float, nullable=False)

    # Calculated results
    co2_saved = Column(Float, nullable=False)
    credits_earned = Column(Float, nullable=False)
    weekly_bonus = Column(Float, nullable=False)

    # Motivation feature
    streak_count = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)