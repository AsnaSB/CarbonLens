import json
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "emission_factors.json")


with open(DATA_PATH, "r") as f:
    EMISSION_FACTORS = json.load(f)


def get_transport_factor(mode: str) -> float:
    return EMISSION_FACTORS["transport"].get(mode.lower(), 0.21)


def get_electricity_factor() -> float:
    return EMISSION_FACTORS["electricity"]["default_grid_factor"]


def get_spending_factor(category: str) -> float:
    spending = EMISSION_FACTORS.get("spending", {})
    return spending.get(category.lower(), spending.get("default", 0))


def get_credit_config():
    return EMISSION_FACTORS["credits"]