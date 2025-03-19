import random

from economy_entity import *
from enterprise_name_generator import trade_good_types
from normalrandom import trade_good_distribution, random_bell_curve




planet_size = 1200
inflation = 1.0
days_elapsed = 0
"""
prices = {}
for t in trade_goods_base_prices:
    prices[t] = []
    for i in range(20):
        price_point = random.triangular(price_distributions[1][0], price_distributions[1][1])
        final_price = round(inflation * price_point * trade_goods_base_prices[t])
        prices[t].append(final_price)

#print(prices)
"""

if __name__ == "__main__":
    # determine trade status, equilibrium quantity and current quantity
    equilibrium = int(input("Input an Equilibrium Supply > "))  # 500
    supply = int(input("Input a Current Supply > "))  # 480

    # market score determines development level, highly developed markets's goods are more expensive
    market_score = float(input("Input a market score (0.8x - 1.2x) > "))
    market = Market.generate_market("Planet", equilibrium, supply, market_score, 0)
