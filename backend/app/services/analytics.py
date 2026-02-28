from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from app.models.event import FootprintEvent


# ---------------------------------------------------
# Date Range Helpers
# ---------------------------------------------------
def _get_date_range(range_type: str):
    now = datetime.utcnow()

    if range_type == "weekly":
        start = now - timedelta(days=7)
        prev_start = start - timedelta(days=7)
    elif range_type == "monthly":
        start = now - timedelta(days=30)
        prev_start = start - timedelta(days=30)
    elif range_type == "yearly":
        start = now - timedelta(days=365)
        prev_start = start - timedelta(days=365)
    else:
        start = None
        prev_start = None

    return start, now, prev_start


# ---------------------------------------------------
# SUMMARY WITH COMPARISON
# ---------------------------------------------------
def get_summary_by_range(db: Session, range_type: str):

    start, end, prev_start = _get_date_range(range_type)

    if not start:
        return {"error": "Invalid range type"}

    # Current Period
    current_total = db.query(
        func.sum(FootprintEvent.co2_kg)
    ).filter(
        FootprintEvent.created_at >= start
    ).scalar() or 0.0

    # Previous Period
    previous_total = db.query(
        func.sum(FootprintEvent.co2_kg)
    ).filter(
        FootprintEvent.created_at >= prev_start,
        FootprintEvent.created_at < start
    ).scalar() or 0.0

    # Breakdown
    breakdown_query = db.query(
        FootprintEvent.category,
        func.sum(FootprintEvent.co2_kg)
    ).filter(
        FootprintEvent.created_at >= start
    ).group_by(
        FootprintEvent.category
    ).all()

    breakdown = {}
    for category, total in breakdown_query:
        breakdown[category] = round(total, 3)

    # Percent share
    percent_share = {}
    if current_total > 0:
        for k, v in breakdown.items():
            percent_share[k] = round((v / current_total) * 100, 2)

    # Hotspot
    hotspot = None
    if breakdown:
        hotspot = max(breakdown, key=breakdown.get)

    # Change %
    change_percent = 0
    if previous_total > 0:
        change_percent = round(
            ((current_total - previous_total) / previous_total) * 100,
            2
        )

    return {
        "range": range_type,
        "current_total_co2": round(current_total, 3),
        "previous_total_co2": round(previous_total, 3),
        "change_percent": change_percent,
        "breakdown_by_category": breakdown,
        "percentage_share": percent_share,
        "top_emission_category": hotspot
    }


# ---------------------------------------------------
# TREND DATA (Daily Aggregation)
# ---------------------------------------------------
def get_trend_data(db: Session, range_type: str):

    start, end, _ = _get_date_range(range_type)

    if not start:
        return {"error": "Invalid range type"}

    results = db.query(
        func.date(FootprintEvent.created_at).label("date"),
        func.sum(FootprintEvent.co2_kg).label("total")
    ).filter(
        FootprintEvent.created_at >= start
    ).group_by(
        func.date(FootprintEvent.created_at)
    ).order_by(
        func.date(FootprintEvent.created_at)
    ).all()

    trend = [
        {
            "date": str(r.date),
            "total_co2": round(r.total, 3)
        }
        for r in results
    ]

    return {
        "range": range_type,
        "trend": trend
    }