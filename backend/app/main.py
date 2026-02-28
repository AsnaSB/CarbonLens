from fastapi import FastAPI

from app.models.db import engine, Base

# Import models so SQLAlchemy registers them
from app.models import event
from app.models import credit

# Import routers
from app.api.routes_events import router as events_router


app = FastAPI(
    title="CarbonLens API",
    description="Backend API for CarbonLens Sustainability Platform",
    version="1.0.0"
)

# Create tables automatically (hackathon style)
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(events_router)


@app.get("/")
def root():
    return {"message": "CarbonLens Backend is Running"}


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "CarbonLens API",
        "version": "1.0.0"
    }