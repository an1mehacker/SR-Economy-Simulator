import math

from prettytable import PrettyTable


def calculate_price_linear(min_multiplier, max_multiplier, current_supply, equilibrium_supply):
    """
    Fixes the linear price calculation so that:
    - Base price is correct at equilibrium supply
    - Price decreases with surplus and increases with deficit
    - Clamped at min multiplier and max multiplier

    :param base_price: int - The base price at equilibrium.
    :param min_multiplier: float - The lowest price multiplier at max surplus.
    :param max_multiplier: float - The highest price multiplier at max deficit.
    :param current_supply: float - The current supply.
    :param equilibrium_supply: float - The stable supply level.

    :return: int - The adjusted price.
    """
    supply_ratio = current_supply / equilibrium_supply  # Ratio of supply to equilibrium
    if supply_ratio >= 1:
        # Surplus: Scale between equilibrium (1.0) and high surplus (e.g., 1.5x equilibrium)
        linear_multiplier = min_multiplier + (1 - min_multiplier) * (equilibrium_supply / current_supply)
    else:
        # Deficit: Scale between equilibrium (1.0) and high deficit (e.g., 0.5x equilibrium)
        linear_multiplier = 1 + (max_multiplier - 1) * (1 - supply_ratio)

    return max(min(linear_multiplier, max_multiplier), min_multiplier)


def calculate_price_logistic(min_multiplier, max_multiplier, current_supply, equilibrium_supply, k=1.5):
    """
    Calculates the price of a commodity based on a logistic supply-demand curve.
    Works well with high supply or negative values.

    :param min_multiplier: float - The lowest price multiplier at maximum surplus.
    :param max_multiplier: float - The highest price multiplier at maximum deficit.
    :param current_supply: float - The current supply of the commodity.
    :param equilibrium_supply: float - The supply level where price is stable.
    :param k: float - Steepness of the curve (higher values create sharper price transitions).

    :return: float - The adjusted price of the commodity.
    """
    supply_ratio = current_supply / equilibrium_supply
    logistic_multiplier = min_multiplier + (max_multiplier - min_multiplier) / (1 + math.exp(-k * (1 - supply_ratio)))
    return logistic_multiplier



# Example Test
lin1 = (calculate_price_linear(0.55, 1.45, 300, 100))
lin2 = (calculate_price_linear(0.55, 1.45, 200, 100))
lin3 = (calculate_price_linear(0.55, 1.45, 50, 100))
lin4 = (calculate_price_linear(0.55, 1.45, 0, 100))
lin5 = (calculate_price_linear(0.55, 1.45, -200, 100))

log1 = (calculate_price_logistic(0.55, 1.45, 300, 100))
log2 = (calculate_price_logistic(0.55, 1.45, 150, 100))
log3 = (calculate_price_logistic(0.55, 1.45, 50, 100))
log4 = (calculate_price_logistic(0.55, 1.45, 0, 100))
log5 = (calculate_price_logistic(0.55, 1.45, -200, 100))

table= PrettyTable(['Supply', "Linear Price", "Logistic Price"])
table.add_row([300, lin1, log1])
table.add_row([200, lin2, log2])
table.add_row([50, lin3, log3])
table.add_row([00, lin4, log4])
table.add_row([-200, lin5, log5])

print(table)

