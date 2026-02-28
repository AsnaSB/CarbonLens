from app.core.emission_factors import get_transport_factor


def calculate_transport_emission(distance_km: float, mode: str) -> float:
    factor = get_transport_factor(mode)
    return round(distance_km * factor, 3)