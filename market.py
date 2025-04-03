import math
import random
from idlelib.window import register_callback

from math2 import lerp, clamp, map_range_clamped
from dataclasses import dataclass

TRADE_GOODS_DATA = {
        "Organics":         {"base_price": 17,  "base_range": 0.40},
        "Synthetics":       {"base_price": 13,  "base_range": 0.35},
        "Common Minerals":  {"base_price": 9,   "base_range": 0.60},
        "Rare Minerals":    {"base_price": 40,  "base_range": 0.50},
        "Refined Minerals": {"base_price": 20,  "base_range": 0.40},
        "Essential Goods":  {"base_price": 22,  "base_range": 0.50},
        "Medicine":         {"base_price": 30,  "base_range": 0.40},
        "Vice Goods":       {"base_price": 30,  "base_range": 0.40},
        "Technology Goods": {"base_price": 60,  "base_range": 0.30},
        "Luxury Goods":     {"base_price": 150, "base_range": 0.25},
        "Weapons":          {"base_price": 75,  "base_range": 0.33},
        "Narcotics":        {"base_price": 300, "base_range": 0.45},
        "Equipment Parts":  {"base_price": 90,  "base_range": 0.15},
        "Fuel":             {"base_price": 10,  "base_range": 0.30},
        "Ammunition":       {"base_price": 15,  "base_range": 0.20},
    }

DEFICIT_SUPPLY_RATIO = 0.75
MAJOR_DEFICIT_SUPPLY_RATIO = 0.2
SURPLUS_SUPPLY_RATIO = 1.25
MAJOR_SURPLUS_SUPPLY_RATIO = 2.0

# it takes 10 000 days to reach 4.0 inflation
MAX_INFLATION_DAYS = 10000
MAX_INFLATION = 4.0

class SimulationStatus(object):
    #This is a singleton
    _instance = None

    def __init__(self):
        self.trade_difficulty = 1
        self.inflation = 1.0
        self.days_elapsed = 0
        self.global_trade_good_status = {
            key: {"price_range": value["base_range"]}
            for key, value in TRADE_GOODS_DATA.items()
        }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SimulationStatus, cls).__new__(cls)
        return cls._instance

    def skip_day(self):
        self.days_elapsed += 1
        self.inflation = lerp(1.0, MAX_INFLATION, clamp(self.days_elapsed / MAX_INFLATION_DAYS, 0, MAX_INFLATION_DAYS))

    def set_to_day(self, day):
        self.days_elapsed = day - 1
        self.skip_day()
        print(self.inflation)

@dataclass
class EconomyEntity:
    """
    :param ee_type: "Enterprise" or "Individual"
    :param name: name of the enterprise like Technology Inc. or if individual John Smith
    """
    ee_type: str
    name: str

@dataclass
class OrderListing:
    price_point: float
    quantity: int
    economy_entity: EconomyEntity
    quality_point: float
    quality: str
    balance_quantity : int = 0
    # when you buy or sell, this amount is added to its sibling order balance quantity where it slowly transfers to quantity

class TradeGoodStatus:
    def __init__(self, essential, legality, max_fluctuation, daily_fluctuation, buy_modifiers, sell_modifiers,
                 equilibrium_quantity, total_supply):
        """
        A status for a trade good that applies to an entire market

        :param essential: 'Non-Essential' or 'Essential'
        :param legality: 'Legal' or 'Illegal'
        :param max_fluctuation: 0.025 for a 5% range. This value is then used to calculate new daily fluctutation
        :param daily_fluctuation: a value between 0.975 and 1.025. Applied both for buy and sell.
        :param buy_modifiers: list of floats, modifiers like random sell-off or deficit event.
        Both this and fluctuation value are all added multiplicatively to the final value.
        :param sell_modifiers: same but for selling
        :param equilibrium_quantity: the total quantity at which the price becomes base price. this value influences
        the final price through a supply and demand logistical function
        """
        self.essential = essential
        self.legality = legality
        self.max_fluctuation = max_fluctuation
        self.daily_fluctuation = daily_fluctuation
        self.buy_modifiers = buy_modifiers
        self.sell_modifiers = sell_modifiers
        self.equilibrium_quantity = equilibrium_quantity
        self.total_supply = total_supply
        self.available_supply = 0

        self.buy_price, self.sell_price = 0, 0

        self.situation = "Idk"

    def calculate_new_daily_fluctuation(self):
        self.daily_fluctuation = random.uniform(1 - self.max_fluctuation, 1 + self.max_fluctuation)

    def get_buy_modifier(self) -> float:
        return self.daily_fluctuation * (math.prod(self.buy_modifiers) if self.buy_modifiers else 1)

    def get_sell_modifier(self) -> float:
        return self.daily_fluctuation * (math.prod(self.sell_modifiers) if self.sell_modifiers else 1)


def calculate_price_logistic(min_multiplier, max_multiplier, supply_ratio, buy_k=0.95, min_sell_discount=0.8,
                             max_sell_discount=0.98, sell_k=10):
    """
    Calculates the price point of a commodity based on a logistic supply-demand curve.
    Works well with high supply or negative values.

    :param min_multiplier: float - The lowest price multiplier at maximum surplus.
    :param max_multiplier: float - The highest price multiplier at maximum deficit.
    :param supply_ratio: Current Supply divided by Equilibrium Supply
    :param buy_k: float - Steepness of the curve (higher values create sharper price transitions).
    Recommend a value of 0.75 - 1.5
    :param min_sell_discount: float - The lowest discount (widest gap in surplus).
    :param max_sell_discount: float - The highest discount (smallest gap in deficit).
    :param sell_k: Similar to buy_k, tends to approach min and max_sell_discount when at low and high supply resp.
    Recommend a value of 5 to 10

    :return: float - The adjusted buy and sell price of the commodity.
    """

    buy_logistic_multiplier = min_multiplier + (max_multiplier - min_multiplier) / (
            1 + math.exp(-buy_k * (1 - supply_ratio)))

    sell_discount = min_sell_discount + (max_sell_discount - min_sell_discount) / (
            1 + math.exp(-sell_k * (1 - supply_ratio)))


    return buy_logistic_multiplier, buy_logistic_multiplier * sell_discount

def trade_good_distribution(total_goods, num_slots, spread_multiplier=0.75):
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


def get_quality_price_multiplier(base_price, quality):
    quality_ranges = {
        'D': (0.80, 0.9) if base_price < 20 else (0.95, 0.975),
        'C': (0.9, 1.0) if base_price < 20 else (0.975, 1.0),
        'B': (1.0, 1.1) if base_price < 20 else (1.0, 1.025),
        'A': (1.0, 1.2) if base_price < 20 else (1.025, 1.05)
    }

    full_range = (0.80, 1.2) if base_price < 20 else (0.95, 1.05)

    # Define the chance of selecting the full range
    full_range_chance = {
        'D': 0.2,
        'C': 0.3,
        'B': 0.3,
        'A': 0.2
    }

    if random.random() < full_range_chance.get(quality, 0):
        base_min, base_max = full_range
    else:
        base_min, base_max = quality_ranges[quality]

    return random.uniform(base_min, base_max)


def bracketed_pricing(equilibrium):
    return (round(MAJOR_DEFICIT_SUPPLY_RATIO * equilibrium), round(DEFICIT_SUPPLY_RATIO * equilibrium),
            round(SURPLUS_SUPPLY_RATIO * equilibrium), round(MAJOR_SURPLUS_SUPPLY_RATIO * equilibrium))

def get_breakpoint_quantities(equilibrium, after_supply, before_supply=100000000):
    # get a list of breakpoint quantites in order of the operation
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

    if after_supply_ratio < MAJOR_DEFICIT_SUPPLY_RATIO <= before_supply_ratio:
        breakpoints.append(a)

    if after_supply_ratio < DEFICIT_SUPPLY_RATIO <= before_supply_ratio:
        breakpoints.append(b)

    if before_supply_ratio > SURPLUS_SUPPLY_RATIO >= after_supply_ratio:
        breakpoints.append(c)

    if before_supply_ratio > MAJOR_SURPLUS_SUPPLY_RATIO >= after_supply_ratio:
        breakpoints.append(d)

    if reverse:
        breakpoints.reverse()

    return breakpoints

def calculate_price_ranges(trade_difficulty):
    global_trade_good_status = SimulationStatus().global_trade_good_status
    max_difficulty_penalty = 0.5  # maximum reduction in price ranges at hardest difficulty

    max_difficulty = 10
    min_difficulty = 1

    for trade_good in global_trade_good_status:
        # higher trade difficulties (value from 1 to 10) = lower profit margins
        base_range = global_trade_good_status[trade_good]["price_range"]

        # in essence, this is a sliding value from max_difficulty_penalty to 1.0 based on the trade difficulty selected
        global_trade_good_status[trade_good]["price_range"] = (base_range *
            map_range_clamped(trade_difficulty, min_difficulty, max_difficulty, 1.0, max_difficulty_penalty))


class Market:
    def __init__(self, market_name, development_score, trade_good_status):
        """

        :param market_name: string - name of the market like the planet or station's name
        :param development_score: a global price modifier, goods are more expensive in highly developed markets
        :param trade_good_status: list of TradeGoodStatus
        """
        self.name = market_name
        self.development_score = development_score
        self.trade_good_status = trade_good_status

        # We can opt to instead of having a collection of EEs, we have a dict of orders for each trade good type like we
        # have with EE and their dict of orders.
        # then an order listing has a reference to an EE instead.
        # This way it's easier to handle orders by type cause we don't have to filter EEs based on their orders
        # we can also easily determine which order belongs to an Enterprise or Individual Corporation

        self.buy_orders = {
            key: []
            for key in TRADE_GOODS_DATA.keys()
        }

        self.sell_orders = {
            key: []
            for key in TRADE_GOODS_DATA.keys()
        }

    def update_available_supply(self, trade_good):
        status = self.trade_good_status[trade_good]
        new_supply = status.total_supply - bracketed_pricing(status.equilibrium_quantity)[1]
        self.trade_good_status[trade_good].available_supply = new_supply if new_supply >= 0 else 0

        ratio = status.total_supply / status.equilibrium_quantity
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
        before_supply = self.trade_good_status[trade_good].total_supply
        self.trade_good_status[trade_good].total_supply += amount
        self.update_available_supply(trade_good)
        self.recalculate_prices(trade_good, "Buy", before_supply, True)

        return amount

    def remove_goods(self, trade_good, amount):
        amount_remaining = amount
        for order in self.buy_orders[trade_good]:
            if amount_remaining <= 0:
                break
            quantity_removed = amount if order.quantity >= amount else order.quantity
            order.quantity = order.quantity - quantity_removed
            amount_remaining -= quantity_removed

        self.trade_good_status[trade_good].total_supply -= amount
        self.update_available_supply(trade_good)

        return amount

    def simulate_prices(self, trade_good, order_index, new_supply_ratio):
        # returns calculated prices at specific supply ratios without affecting anything
        status = self.trade_good_status[trade_good]
        price_range = SimulationStatus().global_trade_good_status[trade_good]["price_range"]
        floor, ceil = 1 - price_range, 1 + price_range

        buy_price, sell_price = calculate_price_logistic(floor, ceil, new_supply_ratio)
        sell_ratio = sell_price / buy_price if buy_price != 0 else 0.9
        sell_price = sell_price * sell_ratio

        buy_order = self.buy_orders[trade_good][order_index]
        sell_order = self.sell_orders[trade_good][order_index]

        return (round(SimulationStatus().inflation * TRADE_GOODS_DATA[trade_good]["base_price"] * buy_price *
                      buy_order.quality_point * self.development_score * status.get_buy_modifier()),
                round(SimulationStatus().inflation * TRADE_GOODS_DATA[trade_good]["base_price"] * sell_price *
                      sell_order.quality_point * self.development_score * status.get_sell_modifier()))

    def recalculate_prices(self, trade_good, operation, before_supply, full_recalculate):
        self.trade_good_status[trade_good].calculate_new_daily_fluctuation()

        if full_recalculate:

            status = self.trade_good_status[trade_good]
            breakpoints = get_breakpoint_quantities(status.equilibrium_quantity, status.total_supply, before_supply)
            breakpoint_quantity = breakpoints[-1] if breakpoints else status.total_supply

            price_range = SimulationStatus().global_trade_good_status[trade_good]["price_range"]
            floor, ceil = 1 - price_range, 1 + price_range
            ratio = breakpoint_quantity / status.equilibrium_quantity if status.equilibrium_quantity != 0 else breakpoint_quantity

            buy_price, sell_price = calculate_price_logistic(floor, ceil, ratio)
            sell_ratio = sell_price / buy_price if buy_price != 0 else 0.9
            sell_price = sell_price * sell_ratio

            self.trade_good_status[trade_good].buy_price, self.trade_good_status[trade_good].sell_price = buy_price, sell_price

            # Only recalculate to the same operation we're executing
            if operation == "Buy":
                for buy_order in self.buy_orders[trade_good]:
                    buy_order.price_point = buy_price * buy_order.quality_point * self.development_score
                    buy_order.calculated_price = self.get_final_price_by_order(buy_order, trade_good, "Buy")

            if operation == "Sell":
                buy_prices = []
                for buy_order in self.buy_orders[trade_good]:
                    buy_prices.append(buy_order.calculated_price)
                minimum_price = min(buy_prices)

                for sell_order in self.sell_orders[trade_good]:
                    sell_order.price_point = sell_price * sell_order.quality_point * self.development_score
                    sell_order.calculated_price = self.get_final_price_by_order(sell_order, trade_good, "Sell", minimum_price)
        else:
            # for normal recalculations must use the old supply
            for buy_order in self.buy_orders[trade_good]:
                buy_order.calculated_price = self.get_final_price_by_order(buy_order, trade_good, "Buy")
            for sell_order in self.sell_orders[trade_good]:
                sell_order.calculated_price = self.get_final_price_by_order(sell_order, trade_good, "Sell")

    def buy_sell(self, orders, order_index, trade_good, quantity, operation):
        try:
            if operation == "Buy":
                order = orders[order_index]
            elif operation == "Sell":
                order = orders[order_index]
            else:
                return -1

            # create pairs for quantity and price
            quantity_operated = quantity if order.quantity >= quantity else order.quantity
            order.quantity = order.quantity - quantity_operated

            before_total = self.trade_good_status[trade_good].total_supply
            before_cost = order.calculated_price

            if operation == "Buy":
                self.buy_orders[trade_good][order_index] = order
                # TODO: with the new Order from EE to Market change, orders stopped being linked to an EE. find a way for this
                self.sell_orders[trade_good][order_index].quantity += quantity_operated


                self.trade_good_status[trade_good].total_supply = self.trade_good_status[trade_good].total_supply - quantity_operated
                self.update_available_supply(trade_good)
            else:
                self.sell_orders[trade_good][order_index] = order
                self.buy_orders[trade_good][order_index].quantity += quantity_operated

                self.trade_good_status[trade_good].total_supply = self.trade_good_status[trade_good].total_supply + quantity_operated
                self.update_available_supply(trade_good)

            # TODO: replace with update function
            ratio = self.trade_good_status[trade_good].total_supply / self.trade_good_status[trade_good].equilibrium_quantity
            if DEFICIT_SUPPLY_RATIO < ratio < SURPLUS_SUPPLY_RATIO:
                situation = "Balanced"
            elif ratio <= DEFICIT_SUPPLY_RATIO:
                situation = "Deficit"
            else:
                situation = "Surplus"

            if ratio <= MAJOR_DEFICIT_SUPPLY_RATIO or ratio >= MAJOR_SURPLUS_SUPPLY_RATIO:
                situation = "Major " + situation

            self.trade_good_status[trade_good].situation = situation
            breakpoints = get_breakpoint_quantities(self.trade_good_status[trade_good].equilibrium_quantity,
                                                    self.trade_good_status[trade_good].total_supply, before_total)

            if breakpoints:
                breakpoint_total = before_total
                # we get the first breakpoint which represents the first portion of the quantities price listed
                quantity = abs(before_total - breakpoints[0])
                order_breakpoint_quantities = [quantity]
                order_breakpoint_prices = [before_cost]

                breakpoint_total -= quantity

                print(breakpoints)
                print(f"Breakpoint reached - recalculating {operation} orders at {breakpoints[-1]} supply!")
                if len(breakpoints) > 1:
                    for i, breakpoint_q in enumerate(breakpoints):
                        if i == len(breakpoints) - 1:
                            quantity = breakpoints[-1] - self.trade_good_status[trade_good].total_supply
                            continue

                        quantity = breakpoint_total - breakpoints[i + 1]
                        breakpoint_total -= quantity

                        # we only need to get the calculated prices, no need to recalculate for every reached breakpoint
                        buy_price, sell_price = self.simulate_prices(trade_good, order_index, breakpoint_q / self.trade_good_status[trade_good].equilibrium_quantity)
                        price = buy_price if operation == "Buy" else sell_price

                        if price == order_breakpoint_prices[i - 1]:
                            # join quantities of the same prices
                            order_breakpoint_quantities[i - 1] += quantity
                        else:
                            order_breakpoint_prices.append(price)
                            order_breakpoint_quantities.append(quantity)

                    self.recalculate_prices(trade_good, operation, before_total, True)
                    order_breakpoint_quantities.append(quantity)
                    order_breakpoint_prices.append(order.calculated_price)
                else:
                    quantity = quantity_operated - quantity
                    self.recalculate_prices(trade_good, operation, before_total, True)
                    order_breakpoint_quantities.append(quantity)
                    order_breakpoint_prices.append(order.calculated_price)

                return order_breakpoint_quantities, order_breakpoint_prices, order

            return [quantity_operated], [before_cost], order
        except IndexError:
            print("Please input a valid corporation index")
            return -1

    def get_final_price_by_order(self, order_listing, trade_good, operation, min_buy_price=1000000):
        if operation == "Buy":
            return round(SimulationStatus().inflation * TRADE_GOODS_DATA[trade_good]["base_price"] *
                         order_listing.price_point * self.trade_good_status[trade_good].get_buy_modifier())
        elif operation == "Sell":
            return min(round(SimulationStatus().inflation * TRADE_GOODS_DATA[trade_good]["base_price"] *
                         order_listing.price_point * self.trade_good_status[trade_good].get_sell_modifier()), min_buy_price)

    @staticmethod
    def generate_market(market_name, equilibrium, supply, market_score):
        trade_status1 = TradeGoodStatus("Non-Essential", "Legal", 0.025, 1,
                                        [], [], 500, 480)

        temp_trade_statuses = {}

        # TODO: Needs a method to create each trade good status based on market's conditions

        for trade_good in TRADE_GOODS_DATA:
            temp_trade_statuses[trade_good] = trade_status1


        temp = Market(market_name, market_score, temp_trade_statuses)
        temp.generate_new_orders(equilibrium, supply, market_score)
        return temp

    def generate_new_orders(self, equilibrium, supply, market_score):

        # TODO: create EEs for all of the remaining trade goods, figure out how to get names of corporations too.
        # for trade_good in TRADE_GOODS_DATA:

        tg = "Technology Goods"
        price_range = SimulationStatus().global_trade_good_status[tg]["price_range"]
        floor, ceil = 1 - price_range, 1 + price_range
        temp_status = TradeGoodStatus("Non-Essential", "Legal", 0.025, 1,
                                      [], [], equilibrium, supply)

        self.trade_good_status[tg] = temp_status

        # allocate supply for an amount of EEs
        # determine spread of prices across all EEs. 0.95x - 1.05x for base prices over 20, under 20 0.8x - 1.2x
        # this spread isn't related to price distributions on main.py as that's how much prices vary over multiple economies
        # create order listings for each EE by using the price spread
        # the price point depends on the quality where the random value tends to the range interval.


        # available supply is what the market offers to export to avoid a player induced deficit by not making available
        # everything to purchase. If Equilibrium is 100, you won't be able to buy enough to cause supply go below
        # 0.75x - 75 units. Meaning the player can only buy from 0.75 ratio and above. However, the price calculations
        # still use of the total supply existing on the market
        internal_supply = True
        available_supply = supply - bracketed_pricing(equilibrium)[1] if internal_supply else supply
        names = ['Lord Technologies', 'Infinity Inc.', 'Celestial Industries', 'Nillaik Systems Ltd.',
                 'Voidware Devices', 'Inilai Electronics', 'Interstellar Circuits']
        enterprise_amount = len(names)

        buy_goods = trade_good_distribution(available_supply, enterprise_amount)

        self.trade_good_status[tg].available_supply = available_supply

        #TODO: Programatically determine amount of enterprise EEs to generate based on market's conditions instead of
        # the hardcoded number 7 we're experimenting. For example more populated developed planets have in general
        # more technology goods corporations. Additionally assign trade good types for EEs immediately

        #qualities = ['D', 'C', 'B', 'A']
        quality_distribution = []
        for i, quantity in enumerate(buy_goods):
            if i < len(buy_goods) * 0.6:  # Top 60% of list
                quality = random.choices(['D', 'C', 'B', 'A'], weights=[0.05, 0.375, 0.475, 0.1])[0]
            else:  # Bottom ~40% of list (lower quantities)
                quality = random.choices(['C', 'B', 'A'], weights=[0.05, 0.475, 0.475])[0]

            quality_distribution.append(quality)

        ratio = supply / equilibrium if equilibrium != 0 else supply
        buy_price, sell_price = calculate_price_logistic(floor, ceil, ratio)
        sell_ratio = sell_price / buy_price if buy_price != 0 else 0.9

        self.trade_good_status[tg].buy_price, self.trade_good_status[tg].sell_price = buy_price, sell_price

        #we adjust the sell price to account for intersection between the lowest buying prices and maximum selling prices
        #higher supply - greater divide between buy and sell price and vice versa
        sell_price = sell_price * sell_ratio

        ees = []
        quality_modifiers = []
        for i in range(enterprise_amount):
            ee = EconomyEntity("Enterprise", names[i])
            ees.append(ee)
            quality_modifier = get_quality_price_multiplier(60, quality_distribution[i])
            quality_modifiers.append(quality_modifier)

        # BUY ORDERS
        buy_final_prices = []
        for i in range(enterprise_amount):
            price_point = buy_price * quality_modifiers[i] * market_score

            buy_order = OrderListing(price_point, buy_goods[i], ees[i], quality_modifiers[i], quality_distribution[i])
            final_price = self.get_final_price_by_order(buy_order, tg, "Buy")
            buy_order.calculated_price = final_price
            buy_order.quality_point = quality_modifiers[i]

            buy_final_prices.append(final_price)
            self.buy_orders[tg].append(buy_order)

        # SELL ORDERS - create sell orders by determining the sell quantity
        # the total quantity for sell orders is determined by 2equilibrium_quantity - quantity
        # the spread is more smoothed out to give the largest producers still a fair amount with spread = 0.4
        sell_goods = trade_good_distribution(2 * equilibrium - supply, 7, 0.4)
        sell_goods.reverse()

        # get the minimum buying price to then establish a maximum selling price
        max_sell_final_price = min(buy_final_prices) - 1

        for i in range(enterprise_amount):
            price_point = sell_price * quality_modifiers[i] * market_score

            sell_order = OrderListing(price_point, sell_goods[i], ees[i], quality_modifiers[i], quality_distribution[i])
            final_price = self.get_final_price_by_order(sell_order, tg, "Sell", max_sell_final_price)
            sell_order.calculated_price = final_price
            sell_order.quality_point = quality_modifiers[i]

            self.sell_orders[tg].append(sell_order)

        if DEFICIT_SUPPLY_RATIO < ratio < SURPLUS_SUPPLY_RATIO:
            situation = "Balanced"
        elif ratio <= DEFICIT_SUPPLY_RATIO:
            situation = "Deficit"
        else:
            situation = "Surplus"

        if ratio <= MAJOR_DEFICIT_SUPPLY_RATIO or ratio >= MAJOR_SURPLUS_SUPPLY_RATIO:
            situation = "Major " + situation

        self.trade_good_status[tg].situation = situation

    def detailed_listing(self, trade_good, debug=True):
        trade_good_status = self.trade_good_status[trade_good]

        buy_orders = self.buy_orders[trade_good]
        sell_orders = self.sell_orders[trade_good]

        if len(buy_orders) == 0 and len(sell_orders) == 0:
            print(f"No orders available for {trade_good}")
            return

        enterprise_amount = len(buy_orders)
        names = [order.economy_entity.name for order in buy_orders]
        quality_distribution = [order.quality for order in buy_orders]

        price_range = SimulationStatus().global_trade_good_status[trade_good]["price_range"]
        floor, ceil = 1 - price_range, 1 + price_range

        max_sell_final_price = min([order.calculated_price for order in buy_orders]) - 1

        print(f"\nDetailed Listing for {trade_good}")
        if debug:
            print(f"Price Ranges: {floor}-{ceil} | Price Points: {round(trade_good_status.buy_price * self.development_score, 2)} "
                  f"{round(trade_good_status.sell_price * self.development_score, 2)} | Min sell:{max_sell_final_price} "
                  f"| Supply Ratio: {trade_good_status.total_supply / trade_good_status.equilibrium_quantity}")

        for i in range(enterprise_amount):
            print(
                f"{str(i + 1) + "."} {names[i]:>25} - Buy (x{buy_orders[i].quantity:<5}) at {buy_orders[i].calculated_price:>4}cr | "
                f"Sell (x{sell_orders[i].quantity:<5}) at {sell_orders[i].calculated_price:>4}cr - Q:{quality_distribution[i]}")

        print(f"Situation - {trade_good_status.situation}")
        print(f"Breakoffs - {bracketed_pricing(trade_good_status.equilibrium_quantity)}")
        print(
            f"Available for export: {trade_good_status.available_supply} | Internal supply: "
            f"{bracketed_pricing(trade_good_status.equilibrium_quantity)[1] - abs(min(0, trade_good_status.available_supply))} "
            f"| Total: {trade_good_status.total_supply}")

        # Filter out invalid (zero-quantity) orders for correct total quantity calculation
        valid_buy_orders = [(order.calculated_price, order.quantity) for order in buy_orders if order.quantity > 0]
        valid_sell_orders = [(order.calculated_price, order.quantity) for order in sell_orders if order.quantity > 0]

        # Calculate total valid quantities
        buy_total_quantity = sum(q for _, q in valid_buy_orders) if valid_buy_orders else 1
        sell_total_quantity = sum(q for _, q in valid_sell_orders) if valid_sell_orders else 1

        # Calculate weighted average price - buying
        buy_weighted_average_price = sum(
            (q / buy_total_quantity) * p for p, q in valid_buy_orders) if valid_buy_orders else \
            (sum(order.calculated_price for order in buy_orders) / len(buy_orders) if buy_orders else 0)
        buy_weighted_average_price = str(round(buy_weighted_average_price)) + "cr"

        # Calculate weighted average price - selling
        sell_weighted_average_price = sum(
            (q / sell_total_quantity) * p for p, q in valid_sell_orders) if valid_sell_orders else \
            (sum(order.calculated_price for order in sell_orders) / len(sell_orders) if sell_orders else 0)
        sell_weighted_average_price = str(round(sell_weighted_average_price)) + "cr"

        # Find min buy price and max sell price, ignoring zero-quantity orders
        if valid_buy_orders:
            min_buy_price = min(valid_buy_orders)[0]
            min_buy_quantity = sum(q for p, q in valid_buy_orders if p == min_buy_price)
        else:
            min_buy_price, min_buy_quantity = (
            min(order.calculated_price for order in buy_orders), 0) if buy_orders else (0, 0)

        if valid_sell_orders:
            max_sell_price = max(valid_sell_orders)[0]
            max_sell_quantity = sum(q for p, q in valid_sell_orders if p == max_sell_price)
        else:
            max_sell_price, max_sell_quantity = (
            max(order.calculated_price for order in sell_orders), 0) if sell_orders else (0, 0)

        min_buy_price = str(min_buy_price) + "cr"
        max_sell_price = str(max_sell_price) + "cr"

        print(f"Average prices: {buy_weighted_average_price}/{sell_weighted_average_price} "
              f"| Min buy: {min_buy_price} (x{min_buy_quantity}) | Max sell: {max_sell_price} (x{max_sell_quantity})")

    def summary_listing(self, tg):
        for i, trade_good in enumerate(self.buy_orders.keys()):
            status = self.trade_good_status[trade_good]
            buy_orders = self.buy_orders[trade_good]
            sell_orders = self.sell_orders[trade_good]

            selected = trade_good == tg

            sell_quantity = sum([order.quantity for order in sell_orders])

            # TODO: remove redundant code as this is copy pasted from detailed listing
            # Filter out invalid (zero-quantity) orders for correct total quantity calculation
            valid_buy_orders = [(order.calculated_price, order.quantity) for order in buy_orders if order.quantity > 0]
            valid_sell_orders = [(order.calculated_price, order.quantity) for order in sell_orders if order.quantity > 0]

            # Calculate total valid quantities
            buy_total_quantity = sum(q for _, q in valid_buy_orders) if valid_buy_orders else 1
            sell_total_quantity = sum(q for _, q in valid_sell_orders) if valid_sell_orders else 1

            # Calculate weighted average price - buying
            buy_weighted_average_price = sum(
                (q / buy_total_quantity) * p for p, q in valid_buy_orders) if valid_buy_orders else \
                (sum(order.calculated_price for order in buy_orders) / len(buy_orders) if buy_orders else 0)
            buy_weighted_average_price = str(round(buy_weighted_average_price)) + "cr"

            # Calculate weighted average price - selling
            sell_weighted_average_price = sum(
                (q / sell_total_quantity) * p for p, q in valid_sell_orders) if valid_sell_orders else \
                (sum(order.calculated_price for order in sell_orders) / len(sell_orders) if sell_orders else 0)
            sell_weighted_average_price = str(round(sell_weighted_average_price)) + "cr"

            print(f"{str(i + 1) + "." + (" >" if selected else ""):<5} {trade_good + (" <" if selected else ""):<20} - "
                  f"Buy (x{status.available_supply:<5}) at ~{buy_weighted_average_price:<6}"
                  f" / Sell (x{sell_quantity:<5}) at ~{sell_weighted_average_price:<6}")