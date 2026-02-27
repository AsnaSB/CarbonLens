from fastapi import FastAPI
from app.models.db import engine, Base
from app.models import event  # this imports event.py (registers model)

app = FastAPI(
    title="CarbonLens API",
    description="Backend API for CarbonLens Sustainability Platform",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "CarbonLens Backend is Running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}