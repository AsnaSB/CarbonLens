from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.deps import get_db
from app.models.event import FootprintEvent
from app.schemas.event_schema import EventCreate, EventOut

from app.schemas.estimate_schema import (
    TransportEstimateRequest,
    TransportEstimateResponse,
    ElectricityEstimateRequest,
    ElectricityEstimateResponse,
    SpendingEstimateRequest,
    SpendingEstimateResponse,
)

# Services
from app.services.transport import calculate_transport_emission
from app.services.electricity import calculate_electricity_emission
from app.services.spending import calculate_spending_emission
from app.services.analytics import get_summary_by_range, get_trend_data
from app.services.credits import compute_weekly_credits

router = APIRouter(prefix="/events", tags=["Events"])

ALLOWED_CATEGORIES = {"transport", "electricity", "spending"}


# ---------------------------------------------------
# CREATE EVENT
# ---------------------------------------------------
@router.post("", response_model=EventOut)
def create_event(payload: EventCreate, db: Session = Depends(get_db)):

    category = payload.category.strip().lower()

    if category not in ALLOWED_CATEGORIES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid category. Use one of: {sorted(ALLOWED_CATEGORIES)}"
        )

    # -------------------------
    # TRANSPORT
    # -------------------------
    if category == "transport":

        if not payload.transport_mode:
            raise HTTPException(
                status_code=400,
                detail="transport_mode is required for transport category"
            )

        co2_kg = calculate_transport_emission(
            payload.value,
            payload.transport_mode.lower()
        )

    # -------------------------
    # ELECTRICITY
    # -------------------------
    elif category == "electricity":

        co2_kg = calculate_electricity_emission(payload.value)

    # -------------------------
    # SPENDING (WITH SUBCATEGORY)
    # -------------------------
    elif category == "spending":

        co2_kg = calculate_spending_emission(
            payload.value,
            payload.spend_category
        )

    # -------------------------
    # SAFETY FALLBACK
    # -------------------------
    else:
        raise HTTPException(
            status_code=400,
            detail="Unhandled category type"
        )

    event = FootprintEvent(
        category=category,
        description=payload.description.strip(),
        value=float(payload.value),
        co2_kg=co2_kg,
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    return event


# ---------------------------------------------------
# LIST EVENTS
# ---------------------------------------------------
@router.get("", response_model=list[EventOut])
def list_events(db: Session = Depends(get_db)):
    return db.query(FootprintEvent).order_by(
        FootprintEvent.created_at.desc()
    ).all()


# ---------------------------------------------------
# ANALYTICS SUMMARY
# ---------------------------------------------------
@router.get("/analytics/summary")
def analytics_summary(
    range: str = Query("weekly", enum=["weekly", "monthly", "yearly"]),
    db: Session = Depends(get_db)
):
    return get_summary_by_range(db, range)


# ---------------------------------------------------
# ANALYTICS TRENDS
# ---------------------------------------------------
@router.get("/analytics/trends")
def analytics_trends(
    range: str = Query("weekly", enum=["weekly", "monthly", "yearly"]),
    db: Session = Depends(get_db)
):
    return get_trend_data(db, range)


# ---------------------------------------------------
# WEEKLY CREDITS
# ---------------------------------------------------
@router.get("/credits/weekly")
def weekly_credits(db: Session = Depends(get_db)):
    return compute_weekly_credits(db)


# ---------------------------------------------------
# ESTIMATE TRANSPORT
# ---------------------------------------------------
@router.post("/estimate/transport", response_model=TransportEstimateResponse)
def estimate_transport(payload: TransportEstimateRequest):

    co2 = calculate_transport_emission(
        payload.distance_km,
        payload.mode
    )

    return {
        "distance_km": payload.distance_km,
        "mode": payload.mode,
        "co2_kg": co2
    }


# ---------------------------------------------------
# ESTIMATE ELECTRICITY
# ---------------------------------------------------
@router.post("/estimate/electricity", response_model=ElectricityEstimateResponse)
def estimate_electricity(payload: ElectricityEstimateRequest):

    co2 = calculate_electricity_emission(payload.kwh)

    return {
        "kwh": payload.kwh,
        "co2_kg": co2
    }


# ---------------------------------------------------
# ESTIMATE SPENDING
# ---------------------------------------------------
@router.post("/estimate/spending", response_model=SpendingEstimateResponse)
def estimate_spending(payload: SpendingEstimateRequest):

    co2 = calculate_spending_emission(
        payload.amount,
        payload.category
    )

    return {
        "amount": payload.amount,
        "category": payload.category,
        "co2_kg": co2
    }