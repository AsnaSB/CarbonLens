from app.core.emission_factors import get_electricity_factor


def calculate_electricity_emission(kwh: float) -> float:
    factor = get_electricity_factor()
    return round(kwh * factor, 3)