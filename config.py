from math2 import map_range_clamped

BASE_PRODUCTION = 200
BASE_CONSUMPTION = 120

TRADE_GOODS_DATA = {
        "Essential Goods":  {"base_price": 22,  "base_range": 0.45, "volatility_price":3,  "volatility_duration": 12,  "base_production": BASE_PRODUCTION / 22},
        "Medicine":         {"base_price": 30,  "base_range": 0.35, "volatility_price":1,  "volatility_duration": 50,  "base_production": BASE_PRODUCTION / 30},
        "Organics":         {"base_price": 17,  "base_range": 0.475, "volatility_price":3,  "volatility_duration": 10, "base_production": BASE_PRODUCTION / 17},
        "Synthetics":       {"base_price": 13,  "base_range": 0.35, "volatility_price":1,  "volatility_duration": 45,  "base_production": BASE_PRODUCTION / 13},
        "Common Minerals":  {"base_price": 9,   "base_range": 0.45, "volatility_price":2,  "volatility_duration": 90,  "base_production": BASE_PRODUCTION / 9},
        "Rare Minerals":    {"base_price": 40,  "base_range": 0.475, "volatility_price":7,  "volatility_duration": 25, "base_production": BASE_PRODUCTION / 40},
        "Refined Minerals": {"base_price": 25,  "base_range": 0.35, "volatility_price":3,  "volatility_duration": 50,  "base_production": BASE_PRODUCTION / 25},
        "Vice Goods":       {"base_price": 30,  "base_range": 0.50, "volatility_price":5,  "volatility_duration": 10,  "base_production": BASE_PRODUCTION / 30},
        "Microchips":       {"base_price": 50,  "base_range": 0.30, "volatility_price":4,  "volatility_duration": 50,  "base_production": BASE_PRODUCTION / 50},
        "Technology Goods": {"base_price": 60,  "base_range": 0.40, "volatility_price":4,  "volatility_duration": 35,  "base_production": BASE_PRODUCTION / 60},
        "Luxury Goods":     {"base_price": 150, "base_range": 0.35, "volatility_price":35, "volatility_duration": 30,  "base_production": BASE_PRODUCTION / 150},
        "Fuel":             {"base_price": 10,  "base_range": 0.30, "volatility_price":1,  "volatility_duration": 15,  "base_production": BASE_PRODUCTION / 10},
        "Ammunition":       {"base_price": 15,  "base_range": 0.30, "volatility_price":2,  "volatility_duration": 20,  "base_production": BASE_PRODUCTION / 15},
        "Equipment Parts":  {"base_price": 90,  "base_range": 0.20, "volatility_price":3,  "volatility_duration": 25,  "base_production": BASE_PRODUCTION / 90},
        "Weapons":          {"base_price": 75,  "base_range": 0.45, "volatility_price":10, "volatility_duration": 20,  "base_production": BASE_PRODUCTION / 75},
        "Narcotics":        {"base_price": 300, "base_range": 0.50, "volatility_price":60, "volatility_duration": 5,   "base_production": BASE_PRODUCTION / 300}
}

MAX_RANGE = max(good["base_range"] for good in TRADE_GOODS_DATA.values())

TRADE_GOOD_ENTERPRISE_RULES = {
    "Organics": {
        "base_amount": 3,
        "politics": {"Democracy": 1, "Republic": 1, "Dictatorship": -1, "Monarchy": -1, "Anarchy": 0, "Theocracy":1},
        "development": {"Agrarian": 2, "Mixed": 0, "Industrial": -1},
    },
    "Synthetics": {
        "base_amount": 3,
        "politics": {"Democracy": 0, "Republic": 1, "Dictatorship": 2, "Monarchy": -1, "Anarchy": 0, "Theocracy":0},
        "development": {"Agrarian": 0, "Mixed": 2, "Industrial": 1},
    },
    "Common Minerals": {
        "base_amount": 4,
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
        "base_amount": 4,
        "politics": {"Democracy": 1, "Republic": 2, "Dictatorship": -1, "Monarchy": -1, "Anarchy": 0, "Theocracy":0},
        "development": {"Agrarian": 3, "Mixed": 0, "Industrial": 0},
    },
    "Medicine": {
        "base_amount": 3,
        "politics": {"Democracy": 2, "Republic": 1, "Dictatorship": 0, "Monarchy": -1, "Anarchy": 0, "Theocracy":-2},
        "development": {"Agrarian": 0, "Mixed": 1, "Industrial": 0},
    },
    "Vice Goods": {
        "base_amount": 2,
        "politics": {"Democracy": 0, "Republic": 0, "Dictatorship": -1, "Monarchy": -1, "Anarchy": 1, "Theocracy":-2},
        "development": {"Agrarian": 0, "Mixed": 1, "Industrial": 0},
    },
    "Technology Goods": {
        "base_amount": 2,
        "politics": {"Democracy": 2, "Republic": 1, "Dictatorship": -1, "Monarchy": 0, "Anarchy": 0, "Theocracy":-10},
        "development": {"Agrarian": -1, "Mixed": 0, "Industrial": 2},
    },
    "Microchips": {
        "base_amount": 2,
        "politics": {"Democracy": 2, "Republic": 1, "Dictatorship": -1, "Monarchy": 0, "Anarchy": 0, "Theocracy":-10},
        "development": {"Agrarian": -1, "Mixed": 0, "Industrial": 2},
    },
    "Luxury Goods": {
        "base_amount": 2,
        "politics": {"Democracy": 1, "Republic": 1, "Dictatorship": 0, "Monarchy": 0, "Anarchy": 1, "Theocracy":2},
        "development": {"Agrarian": -1, "Mixed": 2, "Industrial": 1},
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
        "development": {"Agrarian": 0, "Mixed": 1, "Industrial": 0},
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
LOGISTIC_CUTOFF = 0.05 # ensures min and max prices can be realistically reached

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

BASE_TRADE_GOODS_AMOUNT = 25000 # increases equilibrium, the amount of large volume trades, and decreases their average profitability
EQUILIBRIUM_VARIANCE = 0.25 # doesn't seem to have a great effect on anything
LOW_SUPPLY_SPREAD = -0.25 # greatly affects amount of profitable trades and profitability
HIGH_SUPPLY_SPREAD = 2.25 # greatly affects amount of profitable trades and profitability

# significant effect amount of profitable trades and profitability
INTERSTELLAR_PRICE_SPREAD = 0.20
ENTERPRISE_PRICE_SPREAD = 0.25
INDIVIDUAL_PRICE_SPREAD = 0.40


def get_consumption_multiplier(race, economy, political_system, trade_good, supply_ratio):
    multiplier = 1.0

    if supply_ratio <= MAJOR_DEFICIT_SUPPLY_RATIO:
         multiplier *= 0.2 # demand collapses, rationing is imposed

    # Economy type
    if economy == "Industrial":
        multiplier *= 1.3
    elif economy == "Mixed":
        multiplier *= 1.0
    elif economy == "Agrarian":
        multiplier *= 0.8
    elif economy == "Extractive":
        multiplier *= 0.7

    if trade_good == "Essential Goods":
        multiplier *= 1.5 if race == "Maloq" else 1.0

    # Trade good specific consumption
    if trade_good == "Luxury Goods":
        if race == "Peleng":
            multiplier *= 2
        elif race == "Human":
            multiplier *= 1.5
        elif race == "Faeyan":
            multiplier *= 1.3

    if trade_good == "Vice Goods":
        if race == "Human":
            multiplier *= 1.5
        if race == "Peleng":
            multiplier *= 1.3

    return multiplier

def get_production_multiplier(race, economy, political_system, trade_good, supply_ratio, supply_chain_multiplier, illegal_goods=[]):
    # TODO: ideally replace this with a data table
    base_multiplier = 1.0

    # Economy-based bonuses
    if economy == "Agrarian":
        if trade_good in {"Essential Goods", "Organics"}:
            base_multiplier *= 1.5
        else:
            base_multiplier *= 0.5
    if economy == "Extractive":
        if trade_good in {"Common Minerals", "Rare Minerals"}:
            base_multiplier *= 1.6
        elif trade_good in {"Fuel"}:
            base_multiplier *= 1.3
        else:
            base_multiplier *= 0.4
    if economy == "Industrial":
        if trade_good in {"Equipment Parts", "Technology Goods", "Microchips", "Weapons", "Ammunition", "Refined Minerals"}:
            base_multiplier *= 2
        if race == "Faeyan" and trade_good in ("Microchips", "Technology Goods", "Equipment Parts"):
            base_multiplier *= 1.2
    if economy == "Mixed":
        if trade_good in {"Common Minerals", "Rare Minerals"}:
            base_multiplier *= 1.2
        if trade_good in {"Luxury Goods", "Synthetics", "Vice Goods", "Medicine", "Fuel", "Narcotics"}:
            base_multiplier *= 1.6
        if race == "Human" and trade_good == "Vice Goods":
            base_multiplier *= 1.4
        if race == "Gaalian" and trade_good == "Luxury Goods":
            base_multiplier *= 1.2

    # General Race-based bonuses
    if race == "Peleng":
        if trade_good == "Narcotics":
            base_multiplier *= 1.5
    if race == "Human":
        if trade_good == "Medicine":
            base_multiplier *= 1.2
    if race == "Maloq":
        if trade_good == "Essential Goods":
            base_multiplier *= 2.0
        if trade_good in ("Weapons", "Ammunition"):
            base_multiplier *= 1.2
        if trade_good == "Technology Goods":
            base_multiplier *= 0.7
    if race == "Gaalian":
        if trade_good == "Synthetics":
            base_multiplier *= 1.2
        if trade_good == "Luxury Goods":
            base_multiplier *= 1.2

    if trade_good == "Technology Goods" and political_system == "Theocracy":
        if race != "Faeyan":
            base_multiplier *= 0
        else:
            base_multiplier *= 0.5

    if trade_good in ("Weapons", "Ammunition"):
         base_multiplier *= 1.2 if political_system == "Dictatorship" else 1.0

    if trade_good in illegal_goods:
        if political_system == "Dictatorship":
            base_multiplier *= 0.1  # strict crackdown
        else:
            base_multiplier *= 0.5

    # higher supply ratio -> less production
    # depending on the multiplier calculated, this will balance out with the consumption amount if left running.
    supply_factor = map_range_clamped(supply_ratio, 0, 2, 2, 0.5)
    return base_multiplier * supply_factor * supply_chain_multiplier


def is_legal(trade_good, race, political_system):
    # Absolute legality: Peleng race or Anarchy political system
    if race == "Peleng" or political_system == "Anarchy":
        return True

    if trade_good == "Luxury Goods":
        if race == "Maloq" and political_system != "Monarchy":
            return False

    if trade_good == "Vice Goods":
        if race in {"Maloq", "Gaalian"}:
            return False
        if race == "Faeyan" and political_system in {"Monarchy", "Dictatorship"}:
            return False

    if trade_good == "Technology Goods":
        if race != "Faeyan" and political_system == "Theocracy":
            return False

    if trade_good in {"Weapons", "Ammunition"}:
        if race in {"Faeyan", "Gaalian"} and political_system != "Dictatorship":
            return False
        if race == "Human" and political_system == "Democracy":
            return False

    if trade_good == "Narcotics":
        if race == "Human" and political_system == "Monarchy":
            return True
        if race == "Faeyan" and political_system == "Dictatorship":
            return True

        return False

    # interesting combinations:
    # Maloq Theocracy -> 4 bans: Luxury Goods, Vice Goods, Tech Goods, Narcotics banned
    # Faeyan Dictatorship -> 1 ban: Vice Goods
    # Human Monarchy - Everything legal
    # Combinations that shouldn't exist: Maloq Democracy and Gaalian Anarchy

    return True

def is_essential(trade_good, race):
    return trade_good in ESSENTIAL_GOODS.get(race, set())