import math
import random

from config import *
from math2 import *
from dataclasses import dataclass
from typing import List, Tuple
from name_generator import generate_name, generate_interstellar_corp_names, INTERSTELLAR_CORPOS_BY_RACE


class SimulationStatus(object):
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SimulationStatus, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return  # Already initialized, skip

        self.trade_difficulty_multiplier = 1.0
        self.inflation = 1.0
        self.days_elapsed = 0
        self.trade_difficulty_status = {
            key: {"price_range": value["base_range"]}
            for key, value in TRADE_GOODS_DATA.items()
        }

        self.global_good_status = {
            key: GlobalGoodStatus(value["volatility_price"], value["volatility_duration"], value["base_price"])
            for key, value in TRADE_GOODS_DATA.items()
        }

        self.interstellar_corp_price_multipliers = {}
        for race_dict in INTERSTELLAR_CORPOS_BY_RACE.values():
            for corp_name in race_dict.values():
                if corp_name not in self.interstellar_corp_price_multipliers:
                    self.interstellar_corp_price_multipliers[corp_name] = random.uniform(1 - INTERSTELLAR_PRICE_SPREAD, 1 + INTERSTELLAR_PRICE_SPREAD)

        SimulationStatus._initialized = True

    def get_corp_price_multiplier(self, corp_name):
        if corp_name in self.interstellar_corp_price_multipliers:
            return self.interstellar_corp_price_multipliers[corp_name]

        return -1

    def skip_day(self):
        self.days_elapsed += 1
        new_inflation = clamp(self.days_elapsed / MAX_INFLATION_DAYS, 0, 1.0)
        self.inflation = lerp(1.0, MAX_INFLATION, new_inflation)
        #print(self.inflation)

    def calculate_price_ranges(self, trade_difficulty):
        # only need to be done once
        max_difficulty_penalty = 0.5  # maximum reduction in price ranges at hardest difficulty

        max_difficulty = 10
        min_difficulty = 1

        SimulationStatus().trade_difficulty_multiplier = map_range_clamped(trade_difficulty, min_difficulty,max_difficulty, 1.0,max_difficulty_penalty)

        for trade_good in self.trade_difficulty_status:
            # higher trade difficulties (value from 1 to 10) = lower profit margins
            base_range = self.trade_difficulty_status[trade_good]["price_range"]

            # in essence, this is a sliding value from max_difficulty_penalty to 1.0 based on the trade difficulty selected
            self.trade_difficulty_status[trade_good]["price_range"] = base_range * self.trade_difficulty_multiplier

@dataclass
class Producer:
    """
    :param producer_type: "Interstellar" or "Enterprise" or "Individual"
    :param name: name of the enterprise like Technology Inc. or if individual John Smith
    """
    producer_type: str
    name: str
    price_modifier : float = 1.0

@dataclass
class OrderListing:
    quantity: int
    producer: Producer
    balance_quantity : int = 0
    price_point: float = 1.0
    calculated_price : int = -1

@dataclass
class SellListing:
    quantity: int
    balance_quantity : int = 0
    price_point: float = 1.0
    calculated_price : int = -1

class Item:
    def __init__(self, trade_good, total_quantity: int, breakdown_prices: List[Tuple[int, int]], market_of_origin: str, producer):
        self.trade_good = trade_good
        self.total_quantity = total_quantity
        self.breakdown_prices = breakdown_prices  # List of (quantity, price)
        self.market_of_origin = market_of_origin
        self.producer = producer
        self.total_value = self.calculate_total_cost()

    def calculate_total_quantity(self) -> int:
        return sum(q for q, _ in self.breakdown_prices)

    def calculate_total_cost(self) -> int:
        return sum(q * p for q, p in self.breakdown_prices)

    def get_profit(self):
        return self.total_value

    def is_equal(self, other: 'Item') -> bool:
        return self.trade_good == other.trade_good and self.market_of_origin == other.market_of_origin and self.producer.name == other.producer.name

    def add(self, other: 'Item'):
        if not self.is_equal(other):
            raise ValueError("Cannot add items with different market origins or producers.")

        price_map = {}
        # Merge existing breakdown
        for q, p in self.breakdown_prices:
            price_map[p] = price_map.get(p, 0) + q
        # Add from other
        for q, p in other.breakdown_prices:
            price_map[p] = price_map.get(p, 0) + q

        self.breakdown_prices = [(q, p) for p, q in price_map.items()]
        self.total_quantity = self.calculate_total_quantity()
        self.total_value = self.calculate_total_cost()

    def remove(self, other: 'Item'):
        if not self.is_equal(other):
            raise ValueError("Cannot remove items with different market origins or producers.")

        quantity_to_remove = other.calculate_total_quantity()

        new_breakdown = []
        for q, p in self.breakdown_prices:
            if quantity_to_remove <= 0:
                new_breakdown.append((q, p))
                continue

            if q <= quantity_to_remove:
                quantity_to_remove -= q
                # Skip appending this one — it's fully consumed
            else:
                new_breakdown.append((q - quantity_to_remove, p))
                quantity_to_remove = 0

        self.breakdown_prices = new_breakdown
        self.total_quantity = self.calculate_total_quantity()
        self.total_value = self.calculate_total_cost()

class Actor:
    def __init__(self, money: int):
        self.money = money
        self.items: List[Item] = []

    def find_item_index(self, item: Item) -> int:
        for i, inv_item in enumerate(self.items):
            if inv_item.is_equal(item):
                return i
        return -1

    def add_item(self, item: Item):
        index = self.find_item_index(item)
        if index != -1:
            self.items[index].add(item)
        else:
            self.items.append(item)
        return self

    def remove_item(self, item: Item):
        index = self.find_item_index(item)

        if index != -1:
            if item.total_quantity >= self.items[index].total_quantity:
                del self.items[index]
                return self

            self.items[index].remove(item)
        else:
            print(f"Can't find item: {item.producer}-{item.market_of_origin}")

        return self

    def get_amount_of_items(self, tg):
        count = 0
        for item in self.items:
            if item.trade_good == tg:
                count += 1

        return count

def get_consumption_multiplier(race, economy, political_system, trade_good):
    multiplier = 1.0

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

    if trade_good == "Technology Goods":
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

class MarketGoodStatus:
    def __init__(self, essential : bool, legality : bool, buy_modifiers, sell_modifiers,
                 equilibrium_quantity, total_supply, enterprise_amount):
        """
        A status for a trade good that applies to a single market

        :param essential: 'Non-Essential' or 'Essential'
        :param legality: 'Legal' or 'Illegal'
        :param buy_modifiers: dict of key: Producer, value: additive float bonus like 0.7 -30% when buying
        :param sell_modifiers: same but for selling.
        :param equilibrium_quantity: the total quantity at which the price becomes base price. this value influences
        the final price through a supply and demand logistical function
        """
        self.essential = essential # Whether or not something is essential affects if items return to the producers, if they're essential, they're consumed
        self.legality = legality
        self.buy_modifiers = buy_modifiers
        self.sell_modifiers = sell_modifiers
        self.equilibrium_quantity = equilibrium_quantity
        self.total_supply = total_supply
        self.available_supply = 0
        self.enterprise_amount = enterprise_amount
        self.individual_amount = 0

        # these 2 variables are what is gonna be used to calculate new prices every day. Over time, these values are
        # drifting towards the current supply. When recalculating due to breakpoints, these values change, making big
        # price changes
        self.last_buy_supply = total_supply
        self.last_sell_supply = total_supply

        self.buy_price, self.sell_price = 0, 0

        self.situation = "Idk"

        # FLUCTUATION SUSCEPTIBILITY - new concept, how much of an effect the global fluctuation has on a trade good
        # Growth - lower susceptibility, Recession - higher susceptibility
        # this value should move the fluctuation towards a direction. If it's positive it increases fluct and vice versa
        self.fluctuation_offset = 0.0 #-1.0 to 1.0
        # Equilibrium friction - Allows markets to reject or want certain goods by changing this amount
        self.equilibrium_friction = 1.0

    def get_equilibrium(self):
        return self.equilibrium_quantity * self.equilibrium_friction

class GlobalGoodStatus:
    def __init__(self, max_fluctuation, volatility_duration, base_price):
        """
        A status that applies to the entire simulation, primarily through price fluctuations

        :param max_fluctuation: flat float value. this determines daily fluctuation which is -max_fluctation to +max_fluctuation.
        this value is added at the end of price calculation to all orders
        :param volatility_duration: how often to recalculate the new target fluctuation
        """
        self.base_price = base_price
        self.max_fluctuation = max_fluctuation
        self.current_fluctuation = 0
        self.volatility_duration = volatility_duration
        self.volatility_timer = volatility_duration # reset to 0, otherwise this is just for testing purposes
        self.previous_fluctuation = 0
        self.target_fluctuation = 0

    def __repr__(self):
        return f"Current: {self.current_fluctuation} - Max:{self.max_fluctuation} - Duration:{self.volatility_duration}"

    def calculate_daily_fluctuation(self, statuses : List[MarketGoodStatus]):
        """
        Shifts price fluctuation whether the global economy of that particular trade good is in mostly deficit or surplus
        and with a little variation based on the volatility

        :param statuses - list of all trade good statuses across every market
        """
        self.volatility_timer += 1

        if self.volatility_timer >= self.volatility_duration:
            self.volatility_timer = 0

            # Calculate percentage of list_of_markets in surplus/deficit
            deficit_count = 0
            surplus_count = 0
            for status in statuses:
                if status.situation.lower().find("deficit"):
                    deficit_count += 1
                if status.situation.lower().find("surplus"):
                    surplus_count += 1

            total_markets = len(statuses)

            deficit_ratio = deficit_count / total_markets
            surplus_ratio = surplus_count / total_markets

            variation = self.max_fluctuation / self.base_price

            # Positive if deficit (price rises), Negative if surplus (price falls), naturally clamped to -1 to 1
            net_ratio = deficit_ratio - surplus_ratio + (random.random() * variation)

            self.target_fluctuation = net_ratio * self.max_fluctuation
            self.previous_fluctuation = self.current_fluctuation

        if random.random() < 0.5:
            new_fluctuation = lerp(self.previous_fluctuation, self.target_fluctuation, self.volatility_timer / self.volatility_duration)
            self.current_fluctuation = clamp(new_fluctuation, -self.max_fluctuation, self.max_fluctuation)

def calculate_buy_price(floor, ceil, supply_ratio):
    """
        :param floor: float - The lowest price multiplier at maximum surplus.
        :param ceil: float - The highest price multiplier at maximum deficit.
        :param supply_ratio: Current Supply divided by Equilibrium Supply

        :return: float - The adjusted buy price of the commodity.
        """

    return calculate_buy_price_logistic_impl(floor, ceil, supply_ratio)

def calculate_buy_price_logistic_impl(floor, ceil, supply_ratio):
    # Logistic deviation insures that bottom and max values can be reasonably reached without absurd Logistic factors values.
    new_floor = floor - LOGISTIC_CUTOFF
    new_ceil = ceil + LOGISTIC_CUTOFF

    temp = new_floor + (new_ceil - new_floor) / (1 + math.exp(-BUY_LOGISTIC_FACTOR * (1 - supply_ratio)))

    return clamp(temp, floor, ceil)

def calculate_buy_price_lerp_impl(floor, ceil, supply_ratio) -> float:
    ratio = clamp(supply_ratio, 0, 2)

    return lerp(floor, ceil, 1 - (ratio * 0.5))

def calculate_sell_price_logistic(buy_price, supply_ratio):
    """
    :param buy_price: logistic modifier price of the commodity.
    :param supply_ratio: Current Supply divided by Equilibrium Supply
    """
    discount = SELL_MIN_DISCOUNT + (SELL_MAX_DISCOUNT - SELL_MIN_DISCOUNT) / (1 + math.exp(-SELL_LOGISTIC_FACTOR * (SELL_CENTER_SHIFT - supply_ratio)))

    return buy_price * discount

def trade_good_distribution(total_goods : int, num_slots : int, spread_multiplier=0.75):
    """
    Distributes total_goods into num_slots using a smooth descending pattern with controlled randomness.

    :param total_goods: int - Total amount of goods to distribute.
    :param num_slots: int - Number of slots/entities to distribute among.
    :param spread_multiplier: float - Controls spread smoothness (0.5 for balanced, 1.0 for steep drop-off).
    :return: List[int] - Distributed values in descending order.
    """
    if total_goods <= 0 or num_slots <= 0:
        return [0] * num_slots  # Edge case: No goods to distribute

    # Generate a smooth descending base pattern
    base_pattern = [max(0.1, num_slots - (i * spread_multiplier)) for i in range(num_slots)]
    pattern_sum = sum(base_pattern)

    # Scale pattern to match total_goods
    distribution = [(x / pattern_sum) * total_goods for x in base_pattern]

    # Apply controlled randomness based on available supply
    max_variation = max(1, total_goods // num_slots)  # Ensure reasonable variation
    random_variation = [random.randint(-max_variation, max_variation) for _ in range(num_slots)]

    # Adjust values while preventing negatives
    for i in range(num_slots):
        if i < num_slots // 2:  # Early values get slight positive variation
            distribution[i] += abs(random_variation[i])
        else:  # Later values get slight reductions
            distribution[i] -= abs(random_variation[i]) * 0.25

    # Convert to integers and prevent negatives
    distribution = [max(0, round(x)) for x in distribution]

    # Ensure total sums up correctly
    difference = total_goods - sum(distribution)
    for i in range(abs(difference)):
        if difference > 0:
            distribution[i % num_slots] += 1  # Add to the first elements
        elif difference < 0 < distribution[i % num_slots]:
            distribution[i % num_slots] -= 1  # Remove from nonzero elements

    return distribution

def bracketed_pricing(equilibrium):
    return (round(MAJOR_DEFICIT_SUPPLY_RATIO * equilibrium), round(DEFICIT_SUPPLY_RATIO * equilibrium),
            round(SURPLUS_SUPPLY_RATIO * equilibrium), round(MAJOR_SURPLUS_SUPPLY_RATIO * equilibrium))

def get_breakpoint_quantities(equilibrium, after_supply, before_supply=100000000):
    # get a list of breakpoint quantities in order of the operation
    # the last element of the list represents the new breakpoint quantity that corresponds to after supply
    # the breakpoints selected are always open interval meaning they will only show up if the ratios go 1 value above
    # or below the required.
    # example: eq 500, sup 1200 -> 1000 will not count as reaching 1000 breakpoint only if we got to 999

    a = round(MAJOR_DEFICIT_SUPPLY_RATIO * equilibrium)
    b = round(DEFICIT_SUPPLY_RATIO * equilibrium)
    c = round(SURPLUS_SUPPLY_RATIO * equilibrium)
    d = round(MAJOR_SURPLUS_SUPPLY_RATIO * equilibrium)
    breakpoints = []

    before_supply_ratio = before_supply / equilibrium
    after_supply_ratio = after_supply / equilibrium

    reverse = True
    # clever way to have it work both ways regardless of operation
    if after_supply_ratio > before_supply_ratio:
        temp = after_supply_ratio
        after_supply_ratio = before_supply_ratio
        before_supply_ratio = temp
        reverse = False

    if after_supply_ratio < MAJOR_DEFICIT_SUPPLY_RATIO < before_supply_ratio:
        breakpoints.append(a)

    if after_supply_ratio < DEFICIT_SUPPLY_RATIO < before_supply_ratio:
        breakpoints.append(b)

    if before_supply_ratio > SURPLUS_SUPPLY_RATIO > after_supply_ratio:
        breakpoints.append(c)

    if before_supply_ratio > MAJOR_SURPLUS_SUPPLY_RATIO > after_supply_ratio:
        breakpoints.append(d)

    if reverse:
        breakpoints.reverse()

    return breakpoints

def calculate_final_price(inflation, base_price, price_point, current_fluctuation, bonus, min_price=100000000, fluctuation_multiplier=1.0) -> int:
    return round(min(inflation * base_price * price_point + (current_fluctuation * inflation * fluctuation_multiplier), min_price) * bonus)

class Market:
    def __init__(self, market_name, race, political_system, development_type, market_size, development_score, trade_good_status):
        """

        :param market_name: string - name of the market like the planet or station's name
        :param development_score: a global price modifier, goods are more expensive in highly developed list_of_markets
        :param trade_good_status: list of MarketGoodStatus
        """
        self.name = market_name
        self.race = race
        self.political_system = political_system
        self.development_type = development_type
        self.market_size = market_size
        self.development_score = development_score
        self.trade_good_status = trade_good_status

        # We can opt to instead of having a collection of EEs, we have a dict of orders for each trade good type like we
        # have with producer and their dict of orders.
        # then an order listing has a reference to a producer instead.
        # This way it's easier to handle orders by type because we don't have to filter EEs based on their orders
        # we can also easily determine which order belongs to an Enterprise or Individual Corporation

        self.buy_orders = {
            key: []
            for key in TRADE_GOODS_DATA.keys()
        }

        self.sell_order = {
            key: SellListing(0,0)
            for key in TRADE_GOODS_DATA.keys()
        }

    def consumption_production(self):
        # get illegal goods
        illegal_goods = [name for name, status in self.trade_good_status.items() if not status.legality]

        for trade_good, buy_orders in self.buy_orders.items():
            status = self.trade_good_status[trade_good]
            sell_order = self.sell_order[trade_good]
            supply_ratio = status.total_supply / status.get_equilibrium()

            enterprise_bonus = min(max(0.5, status.enterprise_amount) / TRADE_GOOD_ENTERPRISE_RULES[trade_good]["base_amount"], 1.5)
            supply_chain_multiplier = self.get_supply_chain_multiplier(trade_good)
            consumption = get_consumption_multiplier(self.race, self.development_type, self.political_system, trade_good)
            production = get_production_multiplier(self.race, self.development_type, self.political_system, trade_good, supply_ratio, supply_chain_multiplier, illegal_goods) * enterprise_bonus
            market_size_multiplier = map_range_clamped(self.market_size, 500, 3000, 0.5, 1.5)
            net_production = market_size_multiplier * TRADE_GOODS_DATA[trade_good]["base_production"] * (production - consumption)
            print(f"{trade_good:<20}: {"+" if net_production >= 0 else ""}{round(net_production, 1)} "
                  f"(base:{round(market_size_multiplier * TRADE_GOODS_DATA[trade_good]["base_production"], 1)}"
                  f"|supply chain: {round(supply_chain_multiplier, 1)}|con:{round(consumption, 1)}"
                  f"|prod:{round(production, 1)})|corpo bonus: {round(enterprise_bonus, 2)}")

    def get_supply_chain_multiplier(self, trade_good):
        required = SUPPLY_CHAINS.get(trade_good, set())
        multiplier = 1.0
        if not required:
            return multiplier
        for dependency_trade_good in required:
            status = self.trade_good_status[dependency_trade_good]
            ratio = status.total_supply / status.equilibrium_quantity
            if ratio < DEFICIT_SUPPLY_RATIO:
                ratio = map_range_clamped(ratio, 0, DEFICIT_SUPPLY_RATIO, 0, 1.0)
                multiplier *= ratio
        return multiplier


    def balance_quantities_sell(self):
        balance_factor = 0.075

        for trade_good in TRADE_GOODS_DATA:
            order = self.sell_order[trade_good]
            if order.balance_quantity > 0:
                # Balance out 10% or 3 units whichever is higher until it empties out
                amount_to_shift = min(max(round(order.balance_quantity * balance_factor),3), order.balance_quantity)
                order.balance_quantity -= amount_to_shift
                order.quantity += amount_to_shift

    def balance_quantities(self, trade_good):
        balance_factor = 0.2

        for order in self.buy_orders[trade_good]:
            # balance quantities by 20% or 2 whichever is higher until it empties out
            amount_to_shift = min(max(round(order.balance_quantity * balance_factor),2), order.balance_quantity)
            order.balance_quantity -= amount_to_shift
            order.quantity += amount_to_shift

    def drift_prices(self, trade_good):
        # doesn't actually change prices but sets it up when the prices recalculate
        drift_factor = 0.1
        status = self.trade_good_status[trade_good]

        supply = status.total_supply

        buy_delta = supply - status.last_buy_supply
        self.trade_good_status[trade_good].last_buy_supply += buy_delta * drift_factor

        sell_delta = supply - status.last_sell_supply
        self.trade_good_status[trade_good].last_sell_supply += sell_delta * drift_factor

    def update_available_supply(self, trade_good):
        status = self.trade_good_status[trade_good]
        new_supply = status.total_supply - bracketed_pricing(status.get_equilibrium())[1]
        self.trade_good_status[trade_good].available_supply = new_supply if new_supply >= 0 else 0

        ratio = status.total_supply / status.get_equilibrium()
        if DEFICIT_SUPPLY_RATIO < ratio < SURPLUS_SUPPLY_RATIO:
            situation = "Balanced"
        elif ratio <= DEFICIT_SUPPLY_RATIO:
            situation = "Deficit"
        else:
            situation = "Surplus"

        if ratio <= MAJOR_DEFICIT_SUPPLY_RATIO or ratio >= MAJOR_SURPLUS_SUPPLY_RATIO:
            situation = "Major " + situation

        self.trade_good_status[trade_good].situation = situation

    def add_goods(self, trade_good, ee_index, amount):
        self.buy_orders[trade_good][ee_index].quantity += amount
        self.trade_good_status[trade_good].total_supply += amount
        self.recalculate_prices(trade_good, "Buy", False)
        self.update_available_supply(trade_good)

        return amount

    def remove_goods(self, trade_good, amount):
        amount_remaining = amount
        for order in self.buy_orders[trade_good]:
            if amount_remaining <= 0:
                break
            quantity_removed = amount_remaining if order.quantity >= amount_remaining else order.quantity
            order.quantity = order.quantity - quantity_removed
            amount_remaining -= quantity_removed

        self.trade_good_status[trade_good].total_supply -= amount
        self.trade_good_status[trade_good].last_buy_supply, self.trade_good_status[trade_good].last_sell_supply = self.trade_good_status[trade_good].total_supply, self.trade_good_status[trade_good].total_supply
        self.recalculate_prices(trade_good, "Sell", False)
        self.update_available_supply(trade_good)

        return amount

    def simulate_buy_price(self, trade_good, new_supply_ratio, order_index) -> int:
        order = self.buy_orders[trade_good][order_index]
        price_point = self.calculate_buy_price_point(order, trade_good, new_supply_ratio)
        return calculate_final_price(SimulationStatus().inflation,
                                     TRADE_GOODS_DATA[trade_good]["base_price"],
                                     price_point,
                                     SimulationStatus().global_good_status[trade_good].current_fluctuation,
                                     self.get_buy_price_bonus(order, trade_good))

    def simulate_sell_price(self, trade_good, new_supply_ratio, item : Item) -> int:
        price_point, _ = self.calculate_sell_price_point(trade_good, new_supply_ratio)
        return calculate_final_price(SimulationStatus().inflation,
                                     TRADE_GOODS_DATA[trade_good]["base_price"],
                                     price_point,
                                     SimulationStatus().global_good_status[trade_good].current_fluctuation,
                                     self.get_sell_price_bonus(item, trade_good))

    def recalculate_prices(self, trade_good, operation="Buy", breakpoint_recalculate=True):
        if len(self.buy_orders[trade_good]) == 0:
            return

        status = self.trade_good_status[trade_good]

        last_supply = status.last_buy_supply if operation == "Buy" else status.last_sell_supply
        new_supply = last_supply

        if breakpoint_recalculate:
            breakpoints = get_breakpoint_quantities(status.get_equilibrium(), status.total_supply, last_supply)
            new_supply = breakpoints[-1] if breakpoints else new_supply
            if operation == "Buy":
                status.last_buy_supply = new_supply
                print(f"Last Buy now: {status.last_buy_supply}")
            else:
                status.last_sell_supply = new_supply
                print(f"Last Sell now: {status.last_sell_supply}")

        ratio = new_supply / status.get_equilibrium() if status.get_equilibrium() != 0 else new_supply

        sell_price, buy_price = self.calculate_sell_price_point(trade_good, ratio)

        # Only recalculate to the same operation we're executing otherwise we calculate both
        if operation == "Buy" or not breakpoint_recalculate:
            for buy_order in self.buy_orders[trade_good]:
                buy_order.price_point = self.calculate_buy_price_point(buy_order, trade_good, ratio)
                buy_order.calculated_price = self.get_buy_price_by_order(buy_order, trade_good)

        if operation == "Sell" or not breakpoint_recalculate:
            self.sell_order[trade_good].price_point = sell_price
            self.sell_order[trade_good].calculated_price = self.get_sell_price_by_order(self.sell_order[trade_good], trade_good)

        self.trade_good_status[trade_good].buy_price, self.trade_good_status[trade_good].sell_price = buy_price, sell_price

    def get_bracketed_set(self, trade_good, operation, before_total, before_cost, quantity_operated, order_index=-1, item=None):
        status = self.trade_good_status[trade_good]
        #last_supply = status.last_buy_supply if operation == "Buy" else status.last_sell_supply
        breakpoints = get_breakpoint_quantities(status.get_equilibrium(), status.total_supply, before_total)

        if breakpoints:
            breakpoint_total = before_total
            # we get the first breakpoint which represents the first portion of the quantities price listed
            quantity = abs(before_total - breakpoints[0])
            order_breakpoint_quantities = [quantity]
            order_breakpoint_prices = [before_cost]

            breakpoint_total -= quantity
            quantity_made = quantity_operated

            print(f"Breakpoint reached - recalculating {operation} orders at {breakpoints[-1]} supply!")
            if len(breakpoints) > 1:
                for i, breakpoint_q in enumerate(breakpoints):
                    if i == len(breakpoints) - 1:
                        quantity = quantity_operated - sum(order_breakpoint_quantities)
                        continue

                    quantity = breakpoints[i + 1] - min(breakpoints[i], quantity_made)
                    breakpoint_total -= quantity
                    quantity_made -= quantity

                    # we only need to get the calculated prices, no need to recalculate for every reached breakpoint

                    price = self.simulate_buy_price(trade_good, breakpoint_q / status.get_equilibrium(), order_index) \
                        if operation == "Buy" else self.simulate_sell_price(trade_good, breakpoint_q / status.get_equilibrium(), item)

                    if price == order_breakpoint_prices[i - 1]:
                        # join quantities of the same prices
                        order_breakpoint_quantities[i - 1] += quantity
                    else:
                        order_breakpoint_prices.append(price)
                        order_breakpoint_quantities.append(quantity)

                self.recalculate_prices(trade_good, operation, True)
                order = self.buy_orders[trade_good][order_index] if operation == "Buy" else self.sell_order[trade_good]
                order_breakpoint_quantities.append(quantity)
                order_breakpoint_prices.append(order.calculated_price)
            else:
                quantity = quantity_operated - quantity
                self.recalculate_prices(trade_good, operation, True)
                order = self.buy_orders[trade_good][order_index] if operation == "Buy" else self.sell_order[trade_good]
                order_breakpoint_quantities.append(quantity)
                order_breakpoint_prices.append(order.calculated_price)

            total_cost = 0
            for i, quantity in enumerate(order_breakpoint_quantities):
                total_cost += quantity * order_breakpoint_prices[i]

            return order_breakpoint_quantities, order_breakpoint_prices, total_cost
        return [],[],-1

    def buy(self, trade_good, order_index, quantity) -> Item:
        order = self.buy_orders[trade_good][order_index]

        if order.quantity == 0:
            return Item(trade_good, -1, [], '', None)

        # create pairs for quantity and price
        quantity_operated = quantity if order.quantity >= quantity else order.quantity
        order.quantity = order.quantity - quantity_operated

        before_total = self.trade_good_status[trade_good].total_supply
        before_cost = order.calculated_price

        self.buy_orders[trade_good][order_index] = order
        self.sell_order[trade_good].balance_quantity += quantity_operated

        self.trade_good_status[trade_good].total_supply -= quantity_operated
        self.update_available_supply(trade_good)

        order_breakpoint_quantities, order_breakpoint_prices, total_price = self.get_bracketed_set(
            trade_good, "Buy", before_total, before_cost, quantity_operated, order_index)

        if not order_breakpoint_quantities:
            order_breakpoint_quantities = [quantity_operated]
            order_breakpoint_prices = [before_cost]

        # for an accurate calculation of prices, items retain complete breakdown of quantities and prices
        return Item(trade_good, sum(order_breakpoint_quantities), list(zip(order_breakpoint_quantities, order_breakpoint_prices)), self.name, order.producer)

    def distribute_goods(self, trade_good, old_supply, new_supply):
        # distributes goods to producers with lower order amounts if we're in a surplus situation
        surplus_point = bracketed_pricing(self.trade_good_status[trade_good].get_equilibrium())[2]

        if new_supply <= surplus_point:
            return  # Nothing to distribute

        orders = self.buy_orders[trade_good]
        quantity_to_distribute = new_supply - old_supply if old_supply > surplus_point else new_supply - surplus_point + 1

        if not orders or quantity_to_distribute <= 0:
            return

        weights = []
        total_weight = 0

        for order in orders:
            # Bias factor: gives a bit more weight to smaller-than-average quantities
            bias = max(1 / (math.sqrt(order.quantity + 1)), 1 / (len(orders) * 2))
            randomness = random.uniform(0.8, 1.2)
            weight = bias * randomness
            weights.append(weight)
            total_weight += weight

        # Distribute based on the weights
        distributed_total = 0
        for i, order in enumerate(orders):
            share = round((weights[i] / total_weight) * quantity_to_distribute)

            # Ensure we don't over-distribute
            share = min(share, quantity_to_distribute - distributed_total)
            order.balance_quantity += share
            distributed_total += share

            if distributed_total >= quantity_to_distribute:
                break

    def sell(self, trade_good, item, quantity) -> Item:
        order = self.sell_order[trade_good]

        if item.total_quantity == 0:
            return item

        status = self.trade_good_status[trade_good]
        # create pairs for quantity and price
        quantity_operated = quantity if item.total_quantity >= quantity else item.total_quantity
        quantity_operated = quantity_operated if order.quantity >= quantity_operated else order.quantity
        self.sell_order[trade_good].quantity -= quantity_operated

        before_total = self.trade_good_status[trade_good].total_supply
        before_cost = order.calculated_price

        self.trade_good_status[trade_good].total_supply = status.total_supply + quantity_operated

        self.distribute_goods(trade_good,before_total, self.trade_good_status[trade_good].total_supply)
        self.update_available_supply(trade_good)

        order_breakpoint_quantities, order_breakpoint_prices, total_price = self.get_bracketed_set(
            trade_good, "Sell", before_total, before_cost, quantity_operated, -1, item)

        if not order_breakpoint_quantities:
            order_breakpoint_quantities = [quantity_operated]
            order_breakpoint_prices = [before_cost]

        # Apply same market penalty (SMP)
        if item.market_of_origin == self.name:
            min_price = min([order.calculated_price for order in self.buy_orders[trade_good]]) - 1
            if order.calculated_price > min_price:
                # Sell Price 50
                # Buy prices [49, 50, 51]
                # New price -> 48
                for i, price in enumerate(order_breakpoint_prices):
                    order_breakpoint_prices[i] = clamp(price, 1, min_price)

        return Item(trade_good, quantity_operated, list(zip(order_breakpoint_quantities, order_breakpoint_prices)), item.market_of_origin, item.producer)

    def get_buy_price_bonus(self, order_listing, trade_good) -> float:
        bonuses = self.trade_good_status[trade_good].buy_modifiers

        return bonuses[order_listing.producer] if order_listing.producer.name in bonuses else 1.0

    def get_sell_price_bonus(self, item, trade_good) -> float:
        bonuses = self.trade_good_status[trade_good].sell_modifiers

        return bonuses[item.producer] if item is not None and item.producer.name in bonuses else 1.0

    def get_buy_price_by_order(self, order_listing, trade_good) -> int:
        return calculate_final_price(SimulationStatus().inflation,
                                     TRADE_GOODS_DATA[trade_good]["base_price"],
                                     order_listing.price_point,
                                     SimulationStatus().global_good_status[trade_good].current_fluctuation,
                                     self.get_buy_price_bonus(order_listing, trade_good))

    def get_sell_price_by_order(self, sell_order, trade_good) -> int:
        return calculate_final_price(SimulationStatus().inflation,
                                     TRADE_GOODS_DATA[trade_good]["base_price"],
                                     sell_order.price_point,
                                     SimulationStatus().global_good_status[trade_good].current_fluctuation,
                                     self.get_sell_price_bonus(None, trade_good))

    def calculate_buy_price_point(self, order_listing : OrderListing, trade_good : str, new_supply_ratio=-1) -> float:
        # I'm pretty proud of this as this ensures the resulting price to be strictly within the base range, and it's
        # scaled and adjusted for trade difficulty and the base price range of the trade good
        if trade_good not in TRADE_GOODS_DATA.keys():
            return -1

        base_range = SimulationStatus().trade_difficulty_status[trade_good]["price_range"]
        status = self.trade_good_status[trade_good]
        diff = SimulationStatus().trade_difficulty_multiplier

        range_scaling_multiplier = TRADE_GOODS_DATA[trade_good]["base_range"] / MAX_RANGE

        positive_producer_modifier = abs((1 - order_listing.producer.price_modifier)) if order_listing.producer.price_modifier >= 1.0 else 0
        negative_producer_modifier = abs((1 - order_listing.producer.price_modifier)) if order_listing.producer.price_modifier < 1.0 else 0

        # if these modifiers feel like they're not doing anything to affect the price, raise their maximum range
        positive_development_modifier = abs((1 - self.development_score)) if self.development_score >= 1.0 else 0
        negative_development_modifier = abs((1 - self.development_score)) if self.development_score < 1.0 else 0

        positive_modifiers = abs((positive_producer_modifier + positive_development_modifier) * diff * range_scaling_multiplier)
        negative_modifiers = abs((negative_producer_modifier + negative_development_modifier) * diff * range_scaling_multiplier)

        # this balances out modifiers so that only one of them is applied at the end, pushing the price in a direction
        if positive_modifiers >= negative_modifiers:
            positive_modifiers -= negative_modifiers
            negative_modifiers = 0
        else:
            negative_modifiers -= positive_modifiers
            positive_modifiers = 0

        # for logi function, can be a range of something like 1.20-1.25 or 0.75-0.90 or 0.75-1.25 without modifiers
        floor, ceil = 1 - base_range + positive_modifiers , 1 + base_range - negative_modifiers
        ratio = status.total_supply / status.get_equilibrium() if new_supply_ratio == -1 else new_supply_ratio

        return calculate_buy_price(floor, ceil, ratio)

    def calculate_sell_price_point(self, trade_good : str, new_supply_ratio=-1) -> (float, float):
        if trade_good not in TRADE_GOODS_DATA.keys():
            return -1

        base_range = SimulationStatus().trade_difficulty_status[trade_good]["price_range"]
        status = self.trade_good_status[trade_good]
        diff = SimulationStatus().trade_difficulty_multiplier

        range_scaling_multiplier = TRADE_GOODS_DATA[trade_good]["base_range"] / MAX_RANGE

        # if these modifiers feel like they're not doing anything to affect the price, raise their maximum range
        positive_development_modifier = abs((1 - self.development_score)) if self.development_score >= 1.0 else 0
        negative_development_modifier = abs((1 - self.development_score)) if self.development_score < 1.0 else 0

        positive_modifiers = abs(positive_development_modifier * diff * range_scaling_multiplier)
        negative_modifiers = abs(negative_development_modifier * diff * range_scaling_multiplier)

        # this balances out modifiers so that only one of them is applied at the end, pushing the price in a direction
        if positive_modifiers >= negative_modifiers:
            positive_modifiers -= negative_modifiers
            negative_modifiers = 0
        else:
            negative_modifiers -= positive_modifiers
            positive_modifiers = 0

        ratio = status.total_supply / status.get_equilibrium() if new_supply_ratio == -1 else new_supply_ratio

        floor, ceil = 1 - base_range + positive_modifiers , 1 + base_range - negative_modifiers
        generic_buy_price = calculate_buy_price(floor, ceil, ratio)

        sell_price = calculate_sell_price_logistic(generic_buy_price, ratio)

        return sell_price, generic_buy_price

    @staticmethod
    def generate_market(market_name, race, market_size, development_score, political_system, development_type):
        statuses = {}

        for trade_good in TRADE_GOODS_DATA:
            data = TRADE_GOOD_ENTERPRISE_RULES[trade_good]
            enterprise_amount = int(data["base_amount"] + data["politics"][political_system] + data["development"][development_type])

            base_price = TRADE_GOODS_DATA[trade_good]["base_price"]
            legal = is_legal(trade_good, race, political_system)
            equilibrium_modifier = (max(1, enterprise_amount) / (data["base_amount"] + 1)) if legal else 1

            raw_equilibrium = development_score * BASE_TRADE_GOODS_AMOUNT * equilibrium_modifier * (market_size / 1000) / base_price

            equilibrium = round(random.triangular(1 - EQUILIBRIUM_VARIANCE, 1 + EQUILIBRIUM_VARIANCE) * raw_equilibrium )
            total_supply = round(random.triangular(LOW_SUPPLY_SPREAD, HIGH_SUPPLY_SPREAD) * equilibrium)


            trade_status = MarketGoodStatus(is_essential(trade_good, race), legal, [], [], equilibrium, total_supply, enterprise_amount)
            statuses[trade_good] = trade_status

        temp = Market(market_name, race, political_system, development_type, market_size, development_score, statuses)

        for trade_good in TRADE_GOODS_DATA.keys():
            temp.generate_new_orders(trade_good, race)
        return temp

    def generate_new_orders(self, trade_good, race):
        status = self.trade_good_status[trade_good]
        equilibrium = status.equilibrium_quantity

        if not status.legality:
            interstellar_amount = 0
            enterprise_amount = 0
            interstellar_share, enterprise_share, individual_share = 0, 0, 1.0
        elif status.enterprise_amount <= 0:
            interstellar_amount = 1
            enterprise_amount = 0
            interstellar_share, enterprise_share, individual_share = 0.7, 0, 0.3
        elif status.enterprise_amount <= 4:
            interstellar_amount = 1
            enterprise_amount = status.enterprise_amount - interstellar_amount
            interstellar_share, enterprise_share, individual_share = 0.3, 0.5, 0.2
        else:
            interstellar_amount = 2
            enterprise_amount = status.enterprise_amount - interstellar_amount
            interstellar_share, enterprise_share, individual_share = 0.3, 0.5, 0.2

        individual_amount = int(random.triangular(5, 20))

        # --- Generate total supply scaled to producer count ---
        base_amount = TRADE_GOOD_ENTERPRISE_RULES[trade_good]["base_amount"] + 1
        supply = round(status.total_supply * math.sqrt(max(status.enterprise_amount / base_amount, 1)))
        #supply = round(status.total_supply * math.sqrt(max(status.enterprise_amount, 1) / base_amount))
        #supply = round(status.total_supply * math.sqrt(max(status.enterprise_amount, 1)) / base_amount)
        status.total_supply = supply

        available_supply = supply - bracketed_pricing(equilibrium)[1]
        status.available_supply = available_supply

        # --- Calculate prices ---
        ratio = supply / equilibrium if equilibrium != 0 else supply
        sell_price, buy_price = self.calculate_sell_price_point(trade_good, ratio)
        status.buy_price, status.sell_price = buy_price, sell_price

        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        # --- Distribute goods among producer types based on share ---
        interstellar_goods = trade_good_distribution(round(available_supply * interstellar_share), interstellar_amount, 0.5)
        enterprise_goods = trade_good_distribution(round(available_supply * enterprise_share), enterprise_amount, 0.5)
        individual_goods = trade_good_distribution(round(available_supply * individual_share), individual_amount, 0.5)

        # --- Generate BUY orders for Interstellar producers ---
        interstellar_names = generate_interstellar_corp_names(self.race, trade_good, interstellar_amount)
        for i in range(interstellar_amount):
            corp_name = interstellar_names[i]
            producer = Producer("Interstellar", corp_name, SimulationStatus().get_corp_price_multiplier(corp_name))
            buy_order = OrderListing(interstellar_goods[i], producer)
            buy_order.price_point = self.calculate_buy_price_point(buy_order, trade_good)
            buy_order.calculated_price = self.get_buy_price_by_order(buy_order, trade_good)
            self.buy_orders[trade_good].append(buy_order)

        # --- Generate BUY orders for Enterprise producers ---
        for i in range(enterprise_amount):
            corp_name = f"{self.name}-{trade_good}-E{letters[i % 26]}"
            producer = Producer("Enterprise", corp_name,
                                random.uniform(1 - ENTERPRISE_PRICE_SPREAD, 1 + ENTERPRISE_PRICE_SPREAD))
            buy_order = OrderListing(enterprise_goods[i], producer)
            buy_order.price_point = self.calculate_buy_price_point(buy_order, trade_good)
            buy_order.calculated_price = self.get_buy_price_by_order(buy_order, trade_good)
            self.buy_orders[trade_good].append(buy_order)

        # --- Generate BUY orders for Individual producers ---
        for i in range(int(individual_amount)):
            corp_name = generate_name(race)
            producer = Producer("Individual", corp_name, random.uniform(1 - INDIVIDUAL_PRICE_SPREAD, 1 + INDIVIDUAL_PRICE_SPREAD))
            buy_order = OrderListing(individual_goods[i], producer)
            buy_order.price_point = self.calculate_buy_price_point(buy_order, trade_good)
            buy_order.calculated_price = self.get_buy_price_by_order(buy_order, trade_good)
            self.buy_orders[trade_good].append(buy_order)

        # --- Generate SELL order ---
        self.sell_order[trade_good] = SellListing(2 * equilibrium - supply)
        self.sell_order[trade_good].price_point = sell_price
        self.sell_order[trade_good].calculated_price = self.get_sell_price_by_order(self.sell_order[trade_good], trade_good)

        status.individual_amount = individual_amount
        status.enterprise_text = f"{interstellar_amount}-{enterprise_amount}-{individual_amount}"
        self.update_available_supply(trade_good)

    def detailed_listing(self, trade_good, items, debug=True):
        status = self.trade_good_status[trade_good]

        buy_orders = self.buy_orders[trade_good]
        sell_order = self.sell_order[trade_good]

        if len(buy_orders) == 0 or sell_order is None:
            print(f"No orders available for {trade_good}")
            return

        enterprise_amount = len(buy_orders)
        names = [order.producer.name for order in buy_orders]

        price_range = SimulationStatus().trade_difficulty_status[trade_good]["price_range"]
        floor, ceil = 1 - price_range, 1 + price_range

        #max_sell_final_price = min([order.calculated_price for order in buy_orders]) - 1

        print(f"\nDetailed Listing for {trade_good}")
        if debug:
            print(f"Price Ranges: {round(floor, 2)}-{round(ceil, 2)} | Price Points: {round(status.buy_price, 2)} "
                  f"{round(status.sell_price, 2)} | Last Buy/Sell Amounts:{status.last_buy_supply}/{status.last_sell_supply} "
                  f"| Supply Ratio: {round(status.total_supply / status.get_equilibrium(), 2)} "
                  f"| Today's Fluctuation: {round(SimulationStatus().global_good_status[trade_good].current_fluctuation, 2)}")

        print()
        print(">>" + ("-" * 20) + "BUY" + ("-" * 20) + "<<")
        for i in range(enterprise_amount):
            print(f"{str(i + 1) + ".":>3} {names[i]:<30} - Buy (x{buy_orders[i].quantity:<5}) at {buy_orders[i].calculated_price:>4}cr "
                  f"| In storage: (x{buy_orders[i].balance_quantity})")

        # Filter out invalid (zero-quantity) orders for correct total quantity calculation
        valid_buy_orders = [(order.calculated_price, order.quantity) for order in buy_orders if order.quantity > 0]

        # Calculate total valid quantities
        buy_total_quantity = sum(q for _, q in valid_buy_orders) if valid_buy_orders else 1

        # Calculate weighted average price - buying
        buy_weighted_average_price = sum(
            (q / buy_total_quantity) * p for p, q in valid_buy_orders) if valid_buy_orders else \
            (sum(order.calculated_price for order in buy_orders) / len(buy_orders) if buy_orders else 0)
        buy_weighted_average_price = str(round(buy_weighted_average_price)) + "cr"

        # Find min buy price and max sell price, ignoring zero-quantity orders
        if valid_buy_orders:
            min_buy_price = min(valid_buy_orders)[0]
            min_buy_quantity = sum(q for p, q in valid_buy_orders if p == min_buy_price)
        else:
            min_buy_price, min_buy_quantity = (
                min(order.calculated_price for order in buy_orders), 0) if buy_orders else (0, 0)

        min_buy_price = str(min_buy_price - 1) + "cr"
        min_sell_price = min([order.calculated_price for order in self.buy_orders[trade_good]]) - 1

        print(f"Average buy prices: {buy_weighted_average_price} | Min buy: {min_buy_price} (x{min_buy_quantity})")

        print()
        print(">>" + ("-" * 20) + "SELL" + ("-" * 20) + "<<")
        print(f"Sell (x{sell_order.quantity}) at {sell_order.calculated_price}cr | In storage (x{sell_order.balance_quantity})")

        # TODO List selling bonuses here
        filtered_items = [item for item in items if item.trade_good == trade_good]

        if len(filtered_items) == 0:
            print(f"No {trade_good} to sell")
        for i, item in enumerate(filtered_items):
            if item.market_of_origin == self.name and sell_order.calculated_price > min_sell_price:
                print(f"{i + 1}. - x{item.total_quantity:<5} {item.trade_good} at {round(item.total_value / item.total_quantity)}cr manufactured by {item.producer.name} (Penalty: Same Market Selling -> Sell price {min_sell_price})")
            else:
                print(f"{i + 1}. - x{item.total_quantity:<5} {item.trade_good} at {round(item.total_value / item.total_quantity)}cr manufactured by {item.producer.name}")

        print(f"\nSituation - {status.situation}")
        print(f"Breakoffs - {bracketed_pricing(status.get_equilibrium())}")
        print(
            f"Available for export: {status.available_supply} | Internal supply wanted: "
            f"{bracketed_pricing(status.get_equilibrium())[1] - abs(min(0, status.available_supply))} "
            f"| Total: {status.total_supply}")

    def short_listing(self):
        return f"{self.name} - Size: {self.market_size} - Native Race: {self.race} - Political System: {self.political_system} - Type: {self.development_type} - Development Score: {self.development_score}x"

    def market_listing(self, tg):
        print(self.short_listing())

        print(f"#     Trade good             Buy-Amount  Buy-Price   Producers     Sell-Amount   Sell-Price Situation     Legal   Essential")
        print(f"--------------------------------------------------------------------------------------------------------------------------")

        for i, trade_good in enumerate(self.buy_orders.keys()):
            status = self.trade_good_status[trade_good]
            buy_orders = self.buy_orders[trade_good]
            sell_order = self.sell_order[trade_good]

            selected = trade_good == tg

            # Filter out invalid (zero-quantity) orders for correct total quantity calculation
            valid_buy_orders = [(order.calculated_price, order.quantity) for order in buy_orders if order.quantity > 0]

            # Calculate total valid quantities
            buy_total_quantity = sum(q for _, q in valid_buy_orders) if valid_buy_orders else 1

            # Calculate weighted average price - buying
            buy_weighted_average_price = sum(
                (q / buy_total_quantity) * p for p, q in valid_buy_orders) if valid_buy_orders else \
                (sum(order.calculated_price for order in buy_orders) / len(buy_orders) if buy_orders else 0)

            buy_weighted_average_price = str(round(buy_weighted_average_price)) + "cr"

            print(f"{str(i + 1) + "." + (" >" if selected else ""):<5} {trade_good + (" <" if selected else ""):<20}   "
                  f"x{status.available_supply:<10} ~{buy_weighted_average_price:<10} {status.enterprise_text:<13}"
                  f" x{sell_order.quantity:<12} {str(sell_order.calculated_price) + "cr":<10}"
                  f" {status.situation:<13} {"Yes" if status.legality else "No":<6} "
                  f" {"Yes" if status.essential else "No":<6}")