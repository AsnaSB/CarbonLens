from app.core.emission_factors import get_spending_factor


def calculate_spending_emission(amount: float, category: str = "default") -> float:
    factor = get_spending_factor(category)
    return round(amount * factor, 3)