import math
import random
from math2 import lerp, clamp, map_range_clamped


class SimulationStatus(object):
    # Singleton
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SimulationStatus, cls).__new__(cls)
        return cls.instance

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

    # changes based on trade difficulty so we can reinitialize with different values
    global_trade_good_status = {
        key: {"price_range": value["base_range"]}
        for key, value in TRADE_GOODS_DATA.items()
    }

    trade_difficulty = 1
    inflation = 1.0
    days_elapsed = 0 #we increase inflation every day until we reach 4.0 at 10 000 days
    MAX_INFLATION_DAYS = 10000

    def skip_day(self):
        self.days_elapsed += 1
        self.inflation = lerp(1.0, 4.0, clamp(self.days_elapsed / self.MAX_INFLATION_DAYS, 0, self.MAX_INFLATION_DAYS))

    def set_to_day(self, day):
        self.days_elapsed = day - 1
        self.skip_day()
        print(self.inflation)


class OrderListing:
    def __init__(self, price_point : float, quantity : int, quality='B'):
        """
        Only one order listing per trade good to sell and one to buy for each EconomyEntity
        :param price_point
        :param quantity:
        """
        self.price_point = price_point
        self.quantity = quantity
        self.quality = quality

        self.calculated_price = 0

    def get_price(self, trade_good, modifiers=1):
        simulation = SimulationStatus()
        return simulation.inflation * simulation.TRADE_GOODS_DATA[trade_good][
            "base_price"] * self.price_point * modifiers
    # at worst case scenario the price points can be as low
    # 0.8x market score, 0.975x fluctuation, 0.8x quality modifier, (1 - highest value in trade goods data)x
    # and as high as
    # 1.2x market score, 1.025x fluctuation, 1.2 quality modifier, 1.6x price range
    # this becomes a max theoretical range of 0.25x-2.36x not factoring market modifiers.

class EconomyEntity:
    def __init__(self, ee_type : str, name : str, trade_good_types : list):
        """
        Abbreviated as "ee"
        :param name:
        """
        self.type = ee_type
        self.name = name

        # for each trade good type, we have two orders, one for each operation.
        # only need keys for trade goods that are actually gonna be used
        self.trade_orders = {
            key: {"buy_order": OrderListing(1, 1), "sell_order": OrderListing(1, 1)}
            for key in trade_good_types if key in SimulationStatus().TRADE_GOODS_DATA
        }

    def add_trade_good_type(self, trade_good):
        if trade_good in SimulationStatus().TRADE_GOODS_DATA and trade_good not in self.trade_orders:
            self.trade_orders[trade_good] = {"buy_order": OrderListing(1, 1), "sell_order": OrderListing(1, 1)}

    def find_buy_order(self, trade_good):
        return self.trade_orders[trade_good]["buy_order"]

    def find_sell_order(self, trade_good):
        return self.trade_orders[trade_good]["sell_order"]


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
        elif difference < 0 and distribution[i % num_slots] > 0:
            distribution[i % num_slots] -= 1  # Remove from nonzero elements

    return distribution


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

        # for display
        self.buy_price, self.sell_price = 0, 0

        self.situation = "Idk"

    def calculate_new_daily_fluctuation(self):
        self.daily_fluctuation = random.uniform(1 - self.max_fluctuation, 1 + self.max_fluctuation)

    def get_buy_modifier(self) -> float:
        return self.daily_fluctuation * (math.prod(self.buy_modifiers) if self.buy_modifiers else 1)

    def get_sell_modifier(self) -> float:
        return self.daily_fluctuation * (math.prod(self.sell_modifiers) if self.sell_modifiers else 1)


def get_quality_price_multiplier(base_price, quality):
    """
    Determines a price point multiplier based on quality.
    """
    if base_price >= 20:
        quality_ranges = {
            'D': (0.95, 0.975),
            'C': (0.975, 1.0),
            'B': (1.0, 1.025),
            'A': (1.025, 1.05)
        }
        min_range, max_range = 0.95, 1.05
    else:
        quality_ranges = {
            'D': (0.80, 0.9),
            'C': (0.9, 1.0),
            'B': (1.0, 1.1),
            'A': (1.0, 1.20)
        }
        min_range, max_range = 0.8, 1.2

    base_min, base_max = quality_ranges[quality]

    # Define weights for different ranges (bias towards expected range)
    if quality == 'D':
        return random.choices(
            [random.uniform(base_min, base_max), random.uniform(min_range, max_range)],
            weights=[0.8, 0.2]
        )[0]
    elif quality == 'C':
        return random.choices(
            [random.uniform(base_min, base_max), random.uniform(min_range, max_range)],
            weights=[0.7, 0.3]
        )[0]
    elif quality == 'B':
        return random.choices(
            [random.uniform(base_min, base_max), random.uniform(min_range, max_range)],
            weights=[0.7, 0.3]
        )[0]
    elif quality == 'A':
        return random.choices(
            [random.uniform(base_min, base_max), random.uniform(min_range, max_range)],
            weights=[0.8, 0.2]
        )[0]


def bracketed_pricing(equilibrium):
    # Get breakoff quantity values at 0.75, 0.2, 1.25 and 2
    # Any time those supply ratios are exceeded whether by buying or selling, the prices immediately recalculate
    # in respect to the operation meaning We buy, only buy price gets recalculated, sell, only sell prices etc etc
    # The market will still gradually adjust their prices over a period of 60-70 days.
    # Returns Deficit_Quantity, Major_Deficit_Quantity, Surplus_Quantity, Major_Surplus_Quantity
    return round(0.2 * equilibrium), round(0.75 * equilibrium), round(1.25 * equilibrium), round(2 * equilibrium)

def check_breakpoint_change(equilibrium, before_supply, after_supply) -> bool:
    # True if the change in supply has surpassed a critical breakpoint (positively or negatively)
    breakpoints = bracketed_pricing(equilibrium)
    break_point_1, break_point_2 = 0, 0
    for i, point in enumerate(breakpoints):
        break_point_1 = i if before_supply < point and break_point_1 == 0 else break_point_1
        break_point_2 = i if after_supply < point  and break_point_2 == 0 else break_point_2

    return break_point_1 != break_point_2


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
    def __init__(self, market_name, market_score, economy_entities, trade_good_status):
        """

        :param market_name: string - name of the market like the planet or station's name
        :param market_score: a global price modifier, goods are more expensive in highly developed markets
        :param economy_entities:  list of EconomyEntities
        :param trade_good_status: list of TradeGoodStatus
        """
        self.name = market_name
        self.market_score = market_score
        self.economy_entities = economy_entities
        self.trade_good_status = trade_good_status

    def buy_sell(self, ee_index, trade_good, quantity, operation):
        try:
            if operation == "Buy":
                order = self.economy_entities[ee_index].find_buy_order(trade_good)
            elif operation == "Sell":
                order = self.economy_entities[ee_index].find_sell_order(trade_good)
            else:
                return -1

            quantity_operated = quantity if order.quantity >= quantity else order.quantity
            order.quantity = max(0, order.quantity - quantity)

            if operation == "Buy":
                self.trade_good_status[trade_good].cached_buy_orders[ee_index] = (
                    self.trade_good_status[trade_good].cached_buy_orders[ee_index][0],  # Keep first element
                    order.quantity  # Update second element
                )
                # TODO: add checks to make sure these values don't get weird
                before_total = self.trade_good_status[trade_good].total_supply
                self.trade_good_status[trade_good].total_supply = self.trade_good_status[trade_good].total_supply - quantity_operated
                self.trade_good_status[trade_good].available_supply = self.trade_good_status[trade_good].available_supply - quantity_operated

                if check_breakpoint_change(self.trade_good_status[trade_good].equilibrium_quantity, before_total, self.trade_good_status[trade_good].total_supply):
                    print("Breakpoint reached - recalculate!")

            else:
                self.trade_good_status[trade_good].cached_sell_orders[ee_index] = (
                    self.trade_good_status[trade_good].cached_sell_orders[ee_index][0],  # Keep first element
                    order.quantity  # Update second element
                )
                self.trade_good_status[trade_good].total_supply = self.trade_good_status[trade_good].total_supply + quantity_operated
                self.trade_good_status[trade_good].available_supply = self.trade_good_status[trade_good].available_supply + quantity_operated

            return quantity_operated
        except IndexError:
            print("Please input a valid corporation index")
            return -1

    def get_final_price_by_order(self, order_listing, trade_good, operation, min_buy_price=1000000):
        if operation == "Buy":
            return round(order_listing.get_price(trade_good, self.trade_good_status[trade_good].get_buy_modifier()))
        elif operation == "Sell":
            return min(round(order_listing.get_price(trade_good, self.trade_good_status[trade_good].get_sell_modifier())), min_buy_price)

    def recalculate_prices(self):
        for trade_status in self.trade_good_status:
            self.trade_good_status[trade_status].calculate_new_daily_fluctuation()

    @staticmethod
    def generate_market(market_name, equilibrium, supply, market_score):
        trade_status1 = TradeGoodStatus("Non-Essential", "Legal", 0.025, 1,
                                        [], [], 500, 480)

        trade_data = SimulationStatus().TRADE_GOODS_DATA
        temp_trade_statuses = {}

        for trade_good in trade_data:
            temp_trade_statuses[trade_good] = trade_status1


        temp = Market(market_name, market_score, [], temp_trade_statuses)
        ees = temp.generate_new_ees(equilibrium, supply, market_score, True)
        temp.economy_entities = ees
        return temp

    def generate_new_ees(self, equilibrium, supply, market_score, verbose=True, debug=True):

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

        #we adjust the sell price to account for intersection between the lowest buying prices and maximum selling prices
        #higher supply - greater divide between buy and sell price and vice versa
        sell_price = sell_price * sell_ratio

        ees = []
        quality_modifiers = []
        for i in range(enterprise_amount):
            ee = EconomyEntity("Enterprise", names[i], [tg])
            ees.append(ee)
            quality_modifier = get_quality_price_multiplier(60, quality_distribution[i])
            quality_modifiers.append(quality_modifier)

        # BUY ORDERS
        buy_final_prices = []
        for i in range(enterprise_amount):
            price_point = buy_price * quality_modifiers[i] * market_score

            buy_order = OrderListing(price_point, buy_goods[i], quality_distribution[i])
            final_price = self.get_final_price_by_order(buy_order, tg, "Buy")
            buy_order.calculated_price = final_price

            buy_final_prices.append(final_price)
            ees[i].trade_orders[tg]["buy_order"] = buy_order

        # SELL ORDERS - create sell orders by determining the sell quantity
        # the total quantity for sell orders is determined by 2equilibrium_quantity - quantity
        # the spread is more smoothed out to give the largest producers still a fair amount with spread = 0.4
        sell_goods = trade_good_distribution(2 * equilibrium - supply, 7, 0.4)
        sell_goods.reverse()

        # get the minimum buying price to then establish a maximum selling price
        max_sell_final_price = min(buy_final_prices) - 1

        for i in range(enterprise_amount):
            price_point = sell_price * quality_modifiers[i] * market_score

            sell_order = OrderListing(price_point, sell_goods[i], quality_distribution[i])
            final_price = self.get_final_price_by_order(sell_order, tg, "Sell", max_sell_final_price)
            sell_order.calculated_price = final_price

            ees[i].trade_orders[tg]["sell_order"] = sell_order

        if 0.75 < ratio < 1.25:
            situation = "Balanced"
        elif ratio <= 0.75:
            situation = "Deficit"
        else:
            situation = "Surplus"

        if ratio <= 0.2 or ratio >= 2:
            situation = "Major " + situation

        self.trade_good_status[tg].situation = situation

        return ees

    def detailed_listing(self, trade_good, debug=True):
        trade_good_status = self.trade_good_status[trade_good]

        buy_orders = [ee.trade_orders[trade_good]["buy_order"] for ee in self.economy_entities]
        sell_orders = [ee.trade_orders[trade_good]["sell_order"] for ee in self.economy_entities]
        enterprise_amount = len(self.economy_entities)
        names = [ee.name for ee in self.economy_entities]
        quality_distribution = [order.quality for order in buy_orders]
        situation = trade_good_status.situation

        price_range = SimulationStatus().global_trade_good_status[trade_good]["price_range"]
        floor, ceil = 1 - price_range, 1 + price_range

        max_sell_final_price = min([order.calculated_price for order in buy_orders])

        print(f"Detailed Listing for {trade_good}")
        if debug:
            print(f"Price Ranges: {floor}-{ceil} | Price Points: {round(trade_good_status.buy_price * self.market_score, 2)} {round(trade_good_status.sell_price * self.market_score, 2)} | Min sell:{max_sell_final_price}")

        for i in range(enterprise_amount):
            print(
                f"{str(i + 1) + "."} {names[i]:>25} - Buy (x{buy_orders[i].quantity:<5}) at {buy_orders[i].calculated_price:>4}cr | "
                f"Sell (x{sell_orders[i].quantity:<5}) at {sell_orders[i].calculated_price:>4}cr - Q:{quality_distribution[i]}")

        print(f"Situation - {situation}")
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


