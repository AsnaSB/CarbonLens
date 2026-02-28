from pydantic import BaseModel, Field


# -----------------------------
# TRANSPORT
# -----------------------------
class TransportEstimateRequest(BaseModel):
    distance_km: float = Field(..., ge=0)
    mode: str = Field(..., examples=["car", "bus", "train", "flight"])


class TransportEstimateResponse(BaseModel):
    distance_km: float
    mode: str
    co2_kg: float


# -----------------------------
# ELECTRICITY
# -----------------------------
class ElectricityEstimateRequest(BaseModel):
    kwh: float = Field(..., ge=0)


class ElectricityEstimateResponse(BaseModel):
    kwh: float
    co2_kg: float


# -----------------------------
# SPENDING
# -----------------------------
class SpendingEstimateRequest(BaseModel):
    amount: float = Field(..., ge=0)
    category: str = Field(default="default")


class SpendingEstimateResponse(BaseModel):
    amount: float
    category: str
    co2_kg: float