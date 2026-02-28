# CarbonLens Backend Architecture

## Tech Stack
- FastAPI
- SQLAlchemy
- SQLite (hackathon mode)
- Pydantic
- Uvicorn

## Folder Structure

app/
│
├── api/              # Route definitions
├── core/             # Config & emission factors loader
├── data/             # Emission dataset (JSON)
├── models/           # SQLAlchemy DB models
├── schemas/          # Pydantic schemas
├── services/         # Business logic
├── main.py           # App entry point

## Core Systems

1. Event Engine
Stores carbon footprint activities.

2. Emission Factor Engine
Loads factors from JSON once at startup.

3. Analytics Engine
- Weekly / Monthly / Yearly summaries
- Category breakdown
- Trend aggregation
- Hotspot detection

4. Credits Engine
- Weekly comparison
- CO₂ savings calculation
- Credits + bonus
- Streak tracking

5. Estimate Engine
Instant CO₂ calculation (no DB storage).