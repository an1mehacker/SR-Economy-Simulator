import random

from enterprise_name_generator import trade_good_types
from normalrandom import trade_good_distribution, random_bell_curve

trade_goods = ["Organics", "Synthetics", "Common Minerals", "Rare Minerals",
    "Refined Minerals", "Supplies", "Medicine", "Vice Goods", "Technology Goods",
    "Luxury Goods", "Weapons", "Recreational Drugs", "Equipment Parts", "Fuel",
    "Ammunition"]

trade_goods_base_prices = {
    trade_goods[0] :  17, #Organics
    trade_goods[1] :  13, #Synthetics
    trade_goods[2] :  9,  #Common Minerals
    trade_goods[3]:   40, #Rare Minerals
    trade_goods[4] :  20, #Refined Minerals
    trade_goods[5] :  22, #Supplies
    trade_goods[6] :  30, #Medicine
    trade_goods[7] :  30, #Vice Goods
    trade_goods[8] :  60, #Technology Goods
    trade_goods[9] :  150,#Luxury Goods
    trade_goods[10] : 75, #Weapons
    trade_goods[11] : 300,#Recreational Drugs
    trade_goods[12] : 90, #Equipment Parts
    trade_goods[13] : 10, #Fuel
    trade_goods[14] : 15, #Ammunition
}

# Minimum and maximum price points that can happen across every market
# increments of 0.2 / 9
price_distributions = [
    (0.55, 1.45),   #50%  1
    (0.572, 1.428), #100% 2
    (0.594, 1.405), #150  3
    (0.617, 1.383), #200% 4
    (0.638, 1.361), #250% 5
    (0.661, 1.339), #300% 6
    (0.683, 1.317), #350% 7
    (0.705, 1.294), #400% 8
    (0.728, 1.272), #450% 9
    (0.75, 1.25)    #500% 10
]

planet_size = 1200
inflation = 1.0
days_elapsed = 0

prices = {}
for t in trade_goods_base_prices:
    prices[t] = []
    for i in range(20):
        price_point = random.triangular(price_distributions[1][0], price_distributions[1][1])
        final_price = round(inflation * price_point * trade_goods_base_prices[t])
        prices[t].append(final_price)

#print(prices)
