from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from app.models.event import FootprintEvent
from app.models.credit import CreditLedger
from app.core.emission_factors import get_credit_config


def _get_week_start(date: datetime):
    return date - timedelta(days=date.weekday())


def compute_weekly_credits(db: Session):

    config = get_credit_config()
    credit_unit = config["credit_unit_kg"]
    credit_rate = config["credit_rate"]
    bonus_rate = config["bonus_rate"]

    now = datetime.utcnow()
    current_week_start = _get_week_start(now)
    previous_week_start = current_week_start - timedelta(days=7)

    # ----------------------------
    # Current Week Total
    # ----------------------------
    current_total = db.query(
        func.sum(FootprintEvent.co2_kg)
    ).filter(
        FootprintEvent.created_at >= current_week_start
    ).scalar() or 0.0

    # ----------------------------
    # Previous Week Total
    # ----------------------------
    previous_total = db.query(
        func.sum(FootprintEvent.co2_kg)
    ).filter(
        FootprintEvent.created_at >= previous_week_start,
        FootprintEvent.created_at < current_week_start
    ).scalar() or 0.0

    # ----------------------------
    # Calculate Savings
    # ----------------------------
    co2_saved = max(previous_total - current_total, 0.0)

    credits_earned = (co2_saved / credit_unit) * credit_rate
    weekly_bonus = credits_earned * bonus_rate

    # ----------------------------
    # Streak Logic
    # ----------------------------
    last_record = db.query(CreditLedger).order_by(
        CreditLedger.created_at.desc()
    ).first()

    if last_record and co2_saved > 0:
        streak_count = last_record.streak_count + 1
    elif co2_saved > 0:
        streak_count = 1
    else:
        streak_count = 0

    # ----------------------------
    # Store in Ledger
    # ----------------------------
    new_entry = CreditLedger(
        week_start_date=current_week_start.date(),
        total_co2_week=current_total,
        total_co2_prev_week=previous_total,
        co2_saved=co2_saved,
        credits_earned=round(credits_earned, 3),
        weekly_bonus=round(weekly_bonus, 3),
        streak_count=streak_count
    )

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return {
        "week_start": str(current_week_start.date()),
        "current_week_total": round(current_total, 3),
        "previous_week_total": round(previous_total, 3),
        "co2_saved": round(co2_saved, 3),
        "credits_earned": round(credits_earned, 3),
        "weekly_bonus": round(weekly_bonus, 3),
        "streak_count": streak_count
    }