TRADE_GOODS_DATA = {
        "Essential Goods":  {"base_price": 22,  "base_range": 0.50, "volatility_price":3,  "volatility_duration": 12},
        "Medicine":         {"base_price": 30,  "base_range": 0.40, "volatility_price":1,  "volatility_duration": 50},
        "Organics":         {"base_price": 17,  "base_range": 0.55, "volatility_price":3,  "volatility_duration": 10},
        "Synthetics":       {"base_price": 13,  "base_range": 0.35, "volatility_price":1,  "volatility_duration": 45},
        "Common Minerals":  {"base_price": 9,   "base_range": 0.40, "volatility_price":2,  "volatility_duration": 90},
        "Rare Minerals":    {"base_price": 40,  "base_range": 0.60, "volatility_price":7,  "volatility_duration": 25},
        "Refined Minerals": {"base_price": 25,  "base_range": 0.40, "volatility_price":3,  "volatility_duration": 50},
        "Vice Goods":       {"base_price": 30,  "base_range": 0.40, "volatility_price":5,  "volatility_duration": 10},
        "Microchips":       {"base_price": 50,  "base_range": 0.40, "volatility_price":4,  "volatility_duration": 50},
        "Technology Goods": {"base_price": 60,  "base_range": 0.30, "volatility_price":4,  "volatility_duration": 35},
        "Luxury Goods":     {"base_price": 150, "base_range": 0.25, "volatility_price":30, "volatility_duration": 30},
        "Fuel":             {"base_price": 10,  "base_range": 0.30, "volatility_price":1,  "volatility_duration": 15},
        "Ammunition":       {"base_price": 15,  "base_range": 0.20, "volatility_price":2,  "volatility_duration": 20},
        "Equipment Parts":  {"base_price": 90,  "base_range": 0.15, "volatility_price":3,  "volatility_duration": 25},
        "Weapons":          {"base_price": 75,  "base_range": 0.33, "volatility_price":10, "volatility_duration": 20},
        "Narcotics":        {"base_price": 300, "base_range": 0.45, "volatility_price":60, "volatility_duration": 5}
}

TRADE_GOOD_ENTERPRISE_RULES = {
    "Organics": {
        "base_amount": 4,
        "politics": {"Democracy": 1, "Republic": 1, "Dictatorship": -1, "Monarchy": -1, "Anarchy": 0},
        "development": {"Agrarian": 2, "Mixed": 0, "Industrial": -1},
    },
    "Synthetics": {
        "base_amount": 3,
        "politics": {"Democracy": 2, "Republic": 1, "Dictatorship": -1, "Monarchy": -1, "Anarchy": 0},
        "development": {"Agrarian": 0, "Mixed": 1, "Industrial": 1},
    },
    "Common Minerals": {
        "base_amount": 5,
        "politics": {"Democracy": 1, "Republic": 1, "Dictatorship": -2, "Monarchy": -1, "Anarchy": 1},
        "development": {"Agrarian": 1, "Mixed": 0, "Industrial": -1},
    },
    "Rare Minerals": {
        "base_amount": 2,
        "politics": {"Democracy": 1, "Republic": 1, "Dictatorship": 0, "Monarchy": -1, "Anarchy": 0},
        "development": {"Agrarian": -1, "Mixed": 0, "Industrial": 1},
    },
    "Refined Minerals": {
        "base_amount": 3,
        "politics": {"Democracy": 2, "Republic": 1, "Dictatorship": -1, "Monarchy": -1, "Anarchy": 0},
        "development": {"Agrarian": 0, "Mixed": 0, "Industrial": 1},
    },
    "Essential Goods": {
        "base_amount": 5,
        "politics": {"Democracy": 1, "Republic": 2, "Dictatorship": -1, "Monarchy": -1, "Anarchy": 0},
        "development": {"Agrarian": 1, "Mixed": 0, "Industrial": 0},
    },
    "Medicine": {
        "base_amount": 3,
        "politics": {"Democracy": 2, "Republic": 1, "Dictatorship": 0, "Monarchy": -1, "Anarchy": 0},
        "development": {"Agrarian": 0, "Mixed": 0, "Industrial": 1},
    },
    "Vice Goods": {
        "base_amount": 2,
        "politics": {"Democracy": 0, "Republic": 0, "Dictatorship": -1, "Monarchy": -1, "Anarchy": 1},
        "development": {"Agrarian": 1, "Mixed": 0, "Industrial": 0},
    },
    "Technology Goods": {
        "base_amount": 2,
        "politics": {"Democracy": 2, "Republic": 1, "Dictatorship": -1, "Monarchy": 0, "Anarchy": 0},
        "development": {"Agrarian": -1, "Mixed": 0, "Industrial": 2},
    },
    "Microchips": {
        "base_amount": 1,
        "politics": {"Democracy": 2, "Republic": 1, "Dictatorship": -1, "Monarchy": 0, "Anarchy": 0},
        "development": {"Agrarian": -1, "Mixed": 0, "Industrial": 2},
    },
    "Luxury Goods": {
        "base_amount": 1,
        "politics": {"Democracy": 1, "Republic": 1, "Dictatorship": 0, "Monarchy": 0, "Anarchy": 1},
        "development": {"Agrarian": 0, "Mixed": 0, "Industrial": 1},
    },
    "Weapons": {
        "base_amount": 3,
        "politics": {"Democracy": 0, "Republic": 0, "Dictatorship": 1, "Monarchy": 1, "Anarchy": 1},
        "development": {"Agrarian": 0, "Mixed": 0, "Industrial": 1},
    },
    "Narcotics": {
        "base_amount": 1,
        "politics": {"Democracy": 0, "Republic": -1, "Dictatorship": -2, "Monarchy": -1, "Anarchy": 2},
        "development": {"Agrarian": 1, "Mixed": 0, "Industrial": -1},
    },
    "Equipment Parts": {
        "base_amount": 2,
        "politics": {"Democracy": 1, "Republic": 1, "Dictatorship": -1, "Monarchy": 0, "Anarchy": 0},
        "development": {"Agrarian": -1, "Mixed": 0, "Industrial": 2},
    },
    "Fuel": {
        "base_amount": 4,
        "politics": {"Democracy": 1, "Republic": 1, "Dictatorship": -1, "Monarchy": -1, "Anarchy": 0},
        "development": {"Agrarian": 0, "Mixed": 0, "Industrial": 1},
    },
    "Ammunition": {
        "base_amount": 3,
        "politics": {"Democracy": 0, "Republic": 1, "Dictatorship": 1, "Monarchy": 1, "Anarchy": 1},
        "development": {"Agrarian": 0, "Mixed": 0, "Industrial": 1},
    },
}

ILLEGAL_GOODS_BY_RACE = {
    "Maloq": {"Vice Goods", "Luxury Goods", "Narcotics"},
    "Peleng": set(),  # nothing banned
    "Human": {"Weapons", "Narcotics"},
    "Faeyan": {"Weapons", "Narcotics"},
    "Gaalian": {"Vice Goods", "Narcotics"},
}
ILLEGAL_GOODS_BY_POLITICS = {
    "Democracy": {"Narcotics", "Weapons"},
    "Republic": {"Narcotics"},
    "Dictatorship": {"Narcotics", "Vice Goods"},
    "Monarchy": {"Luxury Goods", "Narcotics"},
    "Anarchy": set(),  # everything goes
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

    "Refined Minerals": {"Common Minerals", "Rare Minerals"},

    "Vice Goods": {"Refined Minerals", "Organics"},
    "Narcotics": {"Refined Minerals", "Organics", "Synthetics"},

    "Luxury Goods": {"Refined Minerals", "Synthetics"},
    "Microchips": {"Refined Minerals", "Synthetics"},
    "Weapons": {"Refined Minerals", "Synthetics"},
    "Ammunition": {"Refined Minerals", "Synthetics"},

    "Technology Goods": {"Microchips", "Synthetics"},

    "Equipment Parts": {"Microchips", "Refined Minerals"},
}

INTERSTELLAR_PRICE_SPREAD = 0.15
ENTERPRISE_PRICE_SPREAD = 0.25
INDIVIDUAL_PRICE_SPREAD = 0.4

DEFICIT_SUPPLY_RATIO = 0.75
MAJOR_DEFICIT_SUPPLY_RATIO = 0.2
SURPLUS_SUPPLY_RATIO = 1.25
MAJOR_SURPLUS_SUPPLY_RATIO = 2.0

# it takes 10 000 days to reach 4.0 inflation
MAX_INFLATION_DAYS = 10000
MAX_INFLATION = 4.0
