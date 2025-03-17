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
    market = Market.generate_market("Planet", 500, 480, 1, 0)
