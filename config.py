TRADE_GOODS_DATA = {
        "Essential Goods":  {"base_price": 22,  "base_range": 0.45, "volatility_price":3,  "volatility_duration": 12},
        "Medicine":         {"base_price": 30,  "base_range": 0.35, "volatility_price":1,  "volatility_duration": 50},
        "Organics":         {"base_price": 17,  "base_range": 0.475, "volatility_price":3,  "volatility_duration": 10},
        "Synthetics":       {"base_price": 13,  "base_range": 0.35, "volatility_price":1,  "volatility_duration": 45},
        "Common Minerals":  {"base_price": 9,   "base_range": 0.45, "volatility_price":2,  "volatility_duration": 90},
        "Rare Minerals":    {"base_price": 40,  "base_range": 0.475, "volatility_price":7,  "volatility_duration": 25},
        "Refined Minerals": {"base_price": 25,  "base_range": 0.35, "volatility_price":3,  "volatility_duration": 50},
        "Vice Goods":       {"base_price": 30,  "base_range": 0.50, "volatility_price":5,  "volatility_duration": 10},
        "Microchips":       {"base_price": 50,  "base_range": 0.30, "volatility_price":4,  "volatility_duration": 50},
        "Technology Goods": {"base_price": 60,  "base_range": 0.40, "volatility_price":4,  "volatility_duration": 35},
        "Luxury Goods":     {"base_price": 150, "base_range": 0.35, "volatility_price":35, "volatility_duration": 30},
        "Fuel":             {"base_price": 10,  "base_range": 0.30, "volatility_price":1,  "volatility_duration": 15},
        "Ammunition":       {"base_price": 15,  "base_range": 0.30, "volatility_price":2,  "volatility_duration": 20},
        "Equipment Parts":  {"base_price": 90,  "base_range": 0.20, "volatility_price":3,  "volatility_duration": 25},
        "Weapons":          {"base_price": 75,  "base_range": 0.45, "volatility_price":10, "volatility_duration": 20},
        "Narcotics":        {"base_price": 300, "base_range": 0.50, "volatility_price":60, "volatility_duration": 5}
}

MAX_RANGE = max(good["base_range"] for good in TRADE_GOODS_DATA.values())

TRADE_GOOD_ENTERPRISE_RULES = {
    "Organics": {
        "base_amount": 4,
        "politics": {"Democracy": 1, "Republic": 1, "Dictatorship": -1, "Monarchy": -1, "Anarchy": 0, "Theocracy":1},
        "development": {"Agrarian": 2, "Mixed": 0, "Industrial": -1},
    },
    "Synthetics": {
        "base_amount": 3,
        "politics": {"Democracy": 0, "Republic": 1, "Dictatorship": 2, "Monarchy": -1, "Anarchy": 0, "Theocracy":0},
        "development": {"Agrarian": 0, "Mixed": 1, "Industrial": 1},
    },
    "Common Minerals": {
        "base_amount": 5,
        "politics": {"Democracy": -1, "Republic": 0, "Dictatorship": 2, "Monarchy": 1, "Anarchy": 0, "Theocracy":1},
        "development": {"Agrarian": 1, "Mixed": 0, "Industrial": -1},
    },
    "Rare Minerals": {
        "base_amount": 2,
        "politics": {"Democracy": 1, "Republic": 1, "Dictatorship": 0, "Monarchy": -1, "Anarchy": 0, "Theocracy":1},
        "development": {"Agrarian": -1, "Mixed": 0, "Industrial": 1},
    },
    "Refined Minerals": {
        "base_amount": 3,
        "politics": {"Democracy": 2, "Republic": 1, "Dictatorship": -1, "Monarchy": -1, "Anarchy": 0, "Theocracy":1},
        "development": {"Agrarian": 0, "Mixed": 0, "Industrial": 1},
    },
    "Essential Goods": {
        "base_amount": 5,
        "politics": {"Democracy": 1, "Republic": 2, "Dictatorship": -1, "Monarchy": -1, "Anarchy": 0, "Theocracy":0},
        "development": {"Agrarian": 1, "Mixed": 0, "Industrial": 0},
    },
    "Medicine": {
        "base_amount": 3,
        "politics": {"Democracy": 2, "Republic": 1, "Dictatorship": 0, "Monarchy": -1, "Anarchy": 0, "Theocracy":-2},
        "development": {"Agrarian": 0, "Mixed": 0, "Industrial": 1},
    },
    "Vice Goods": {
        "base_amount": 2,
        "politics": {"Democracy": 0, "Republic": 0, "Dictatorship": -1, "Monarchy": -1, "Anarchy": 1, "Theocracy":-2},
        "development": {"Agrarian": 1, "Mixed": 0, "Industrial": 0},
    },
    "Technology Goods": {
        "base_amount": 2,
        "politics": {"Democracy": 2, "Republic": 1, "Dictatorship": -1, "Monarchy": 0, "Anarchy": 0, "Theocracy":-10},
        "development": {"Agrarian": -1, "Mixed": 0, "Industrial": 2},
    },
    "Microchips": {
        "base_amount": 1,
        "politics": {"Democracy": 2, "Republic": 1, "Dictatorship": -1, "Monarchy": 0, "Anarchy": 0, "Theocracy":-10},
        "development": {"Agrarian": -1, "Mixed": 0, "Industrial": 2},
    },
    "Luxury Goods": {
        "base_amount": 1,
        "politics": {"Democracy": 1, "Republic": 1, "Dictatorship": 0, "Monarchy": 0, "Anarchy": 1, "Theocracy":2},
        "development": {"Agrarian": 0, "Mixed": 0, "Industrial": 1},
    },
    "Weapons": {
        "base_amount": 3,
        "politics": {"Democracy": 0, "Republic": 0, "Dictatorship": 1, "Monarchy": 1, "Anarchy": 1, "Theocracy":-1},
        "development": {"Agrarian": 0, "Mixed": 0, "Industrial": 1},
    },
    "Narcotics": {
        "base_amount": 1,
        "politics": {"Democracy": 0, "Republic": -1, "Dictatorship": -2, "Monarchy": -1, "Anarchy": 2, "Theocracy":-1},
        "development": {"Agrarian": 1, "Mixed": 0, "Industrial": -1},
    },
    "Equipment Parts": {
        "base_amount": 2,
        "politics": {"Democracy": 1, "Republic": 1, "Dictatorship": -1, "Monarchy": 0, "Anarchy": 0, "Theocracy":-10},
        "development": {"Agrarian": -1, "Mixed": 0, "Industrial": 2},
    },
    "Fuel": {
        "base_amount": 4,
        "politics": {"Democracy": 1, "Republic": 1, "Dictatorship": -1, "Monarchy": -1, "Anarchy": 0, "Theocracy":-1},
        "development": {"Agrarian": 0, "Mixed": 0, "Industrial": 1},
    },
    "Ammunition": {
        "base_amount": 3,
        "politics": {"Democracy": 0, "Republic": 1, "Dictatorship": 1, "Monarchy": 1, "Anarchy": 1, "Theocracy":-1},
        "development": {"Agrarian": 0, "Mixed": 0, "Industrial": 1},
    },
}

ESSENTIAL_GOODS = {
    "Maloq": {"Essential Goods"},
    "Peleng": {"Essential Goods", "Medicine", "Narcotics"},
    "Human": {"Essential Goods", "Medicine", "Vice Goods"},
    "Faeyan": {"Essential Goods", "Medicine", "Technology Goods"},
    "Gaalian": {"Essential Goods", "Medicine"},
}

SUPPLY_CHAINS = {
    "Essential Goods": {"Organics", "Synthetics"},
    "Medicine": {"Organics", "Synthetics"},
    "Vice Goods": {"Organics", "Synthetics"},

    "Refined Minerals": {"Common Minerals", "Rare Minerals"},

    "Narcotics": {"Common Minerals", "Organics", "Synthetics"},

    "Luxury Goods": {"Refined Minerals", "Synthetics"},
    "Microchips": {"Refined Minerals", "Synthetics"},
    "Weapons": {"Refined Minerals", "Synthetics"},
    "Ammunition": {"Refined Minerals", "Synthetics"},

    "Technology Goods": {"Microchips", "Synthetics"},

    "Equipment Parts": {"Microchips", "Refined Minerals"},
}

# General Rules

# The first 3 settings have the greatest effect on amount of profitable trades, affects minimum and maximum prices of trade goods
# only used if the implementation of buy prices uses the logistic function
# To understand the effect these values have on prices, feel free to run the logistic_price_visualizer.py
BUY_LOGISTIC_FACTOR = 3
SELL_LOGISTIC_FACTOR = 2.9
LOGISTIC_CUTOFF = 0.07 # ensures min and max prices can be realistically reached

# Sell
SELL_CENTER_SHIFT = 1.6 # ensures sell prices are not too far away from buy prices, keep the values between 1.0-2.0
SELL_MIN_DISCOUNT = 0.15   # lowest discount (widest gap in surplus)
SELL_MAX_DISCOUNT = 1 # highest discount (smallest gap in deficit)

# changing these doesn't seem to have a great effect on anything
DEFICIT_SUPPLY_RATIO = 0.75
MAJOR_DEFICIT_SUPPLY_RATIO = 0.2
SURPLUS_SUPPLY_RATIO = 1.25
MAJOR_SURPLUS_SUPPLY_RATIO = 2

# it takes 10 000 days to reach 4.0 inflation
MAX_INFLATION_DAYS = 10000
MAX_INFLATION = 4.0

# Market Generation Rules

# higher interval - lower average profits, small effect
LOWER_DEVELOPMENT_SCORE = 0.8
UPPER_DEVELOPMENT_SCORE = 1.2

BASE_TRADE_GOODS_AMOUNT = 20000 # increases the amount of large volume trades and decreases their average profitability
EQUILIBRIUM_VARIANCE = 0.25 # doesn't seem to have a great effect on anything
LOW_SUPPLY_SPREAD = -0.25 # greatly affects amount of profitable trades and profitability
HIGH_SUPPLY_SPREAD = 2.25 # greatly affects amount of profitable trades and profitability

# significant effect amount of profitable trades and profitability
INTERSTELLAR_PRICE_SPREAD = 0.20
ENTERPRISE_PRICE_SPREAD = 0.25
INDIVIDUAL_PRICE_SPREAD = 0.40

"""
f 0 0 5000 (0.2%)
f 0 0 10000 (0.1%)
f 0.2 0.1 (0.4%)

# Market Generation
BASE_TRADE_GOODS_AMOUNT = 25000
EQUILIBRIUM_VARIANCE = 0.5
LOW_SUPPLY_SPREAD = -0.5
HIGH_SUPPLY_SPREAD = 2.5

INTERSTELLAR_PRICE_SPREAD = 0.20
ENTERPRISE_PRICE_SPREAD = 0.25
INDIVIDUAL_PRICE_SPREAD = 0.40
"""

"""
f 0 0 5000 (0.2%)
f 0 0 10000 (0.1%)
f 0.2 0.1 (0.4%)

DEFICIT_SUPPLY_RATIO = 0.75
MAJOR_DEFICIT_SUPPLY_RATIO = 0.5
SURPLUS_SUPPLY_RATIO = 1.5
MAJOR_SURPLUS_SUPPLY_RATIO = 2.5

# it takes 10 000 days to reach 4.0 inflation
MAX_INFLATION_DAYS = 10000
MAX_INFLATION = 4.0

# Market Generation
BASE_TRADE_GOODS_AMOUNT = 25000
EQUILIBRIUM_VARIANCE = 0.5
LOW_SUPPLY_SPREAD = -0.5
HIGH_SUPPLY_SPREAD = 2.5

INTERSTELLAR_PRICE_SPREAD = 0.20
ENTERPRISE_PRICE_SPREAD = 0.25
INDIVIDUAL_PRICE_SPREAD = 0.40"""

"""
f 0 0 5000 (1.5%)
f 0 0 10000 (0.7%)
f 0.2 0.1 (2.5%)

DEFICIT_SUPPLY_RATIO = 0.75
MAJOR_DEFICIT_SUPPLY_RATIO = 0.2
SURPLUS_SUPPLY_RATIO = 1.25
MAJOR_SURPLUS_SUPPLY_RATIO = 2

# Market Generation
BASE_TRADE_GOODS_AMOUNT = 25000
EQUILIBRIUM_VARIANCE = 0.5
LOW_SUPPLY_SPREAD = -3
HIGH_SUPPLY_SPREAD = 5"""

"""
1.4 - 30.9
0.7 - 35.4
0.7 - 33.9

BASE_TRADE_GOODS_AMOUNT = 100000 # increases the amount of large volume trades but not their
EQUILIBRIUM_VARIANCE = 0.5"""

"""
0.3 - 36.6
0.1 - 43.7
0.7 - 32.7

BASE_TRADE_GOODS_AMOUNT = 30000 # increases the amount of large volume trades but not their
EQUILIBRIUM_VARIANCE = 0.5"""

"""
0.4 - 37.8
0.1 - 43.1
0.7 - 33.9

BASE_TRADE_GOODS_AMOUNT = 30000 # increases the amount of large volume trades but not their
EQUILIBRIUM_VARIANCE = 0.05"""
"""
0.6 40.8
0.2  47.9
1.1 36.8
# Market Generation Rules
LOWER_DEVELOPMENT_SCORE = 0.7
UPPER_DEVELOPMENT_SCORE = 1.3"""

"""
0.7 42.3
0.3 50.0
1.1 36.7

LOWER_DEVELOPMENT_SCORE = 0.9
UPPER_DEVELOPMENT_SCORE = 1.1"""
