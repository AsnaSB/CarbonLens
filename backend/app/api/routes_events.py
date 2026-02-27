from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.deps import get_db
from app.models.event import FootprintEvent
from app.schemas.event_schema import EventCreate, EventOut

router = APIRouter(prefix="/events", tags=["Events"])

ALLOWED_CATEGORIES = {"transport", "electricity", "spending"}

@router.post("", response_model=EventOut)
def create_event(payload: EventCreate, db: Session = Depends(get_db)):
    category = payload.category.strip().lower()
    if category not in ALLOWED_CATEGORIES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid category. Use one of: {sorted(ALLOWED_CATEGORIES)}"
        )

    event = FootprintEvent(
        category=category,
        description=payload.description.strip(),
        value=float(payload.value),
        co2_kg=float(payload.co2_kg),
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

@router.get("", response_model=list[EventOut])
def list_events(db: Session = Depends(get_db)):
    return db.query(FootprintEvent).order_by(FootprintEvent.created_at.desc()).all()