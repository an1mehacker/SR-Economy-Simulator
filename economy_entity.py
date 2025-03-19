import math
import random
from hashlib import algorithms_available

#import main
from prettytable import PrettyTable
import normalrandom

inflation = 1.0

# static
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
    "Equipment Parts":  {"base_price": 90,  "base_range": 0.20},
    "Fuel":             {"base_price": 10,  "base_range": 0.30},
    "Ammunition":       {"base_price": 15,  "base_range": 0.15},
}

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
        "Equipment Parts":  {"base_price": 90,  "base_range": 0.20},
        "Fuel":             {"base_price": 10,  "base_range": 0.30},
        "Ammunition":       {"base_price": 15,  "base_range": 0.15},
    }

    # changes based on trade difficulty
    global_trade_good_status = {
        "Organics": {"price_range": 0.40},
        "Synthetics": {"price_range": 0.35},
        "Common Minerals": {"price_range": 0.60},
        "Rare Minerals": {"price_range": 0.50},
        "Refined Minerals": {"price_range": 0.40},
        "Essential Goods": {"price_range": 0.50},
        "Medicine": {"price_range": 0.40},
        "Vice Goods": {"price_range": 0.40},
        "Technology Goods": {"price_range": 0.30},
        "Luxury Goods": {"price_range": 0.25},
        "Weapons": {"price_range": 0.33},
        "Narcotics": {"price_range": 0.45},
        "Equipment Parts": {"price_range": 0.20},
        "Fuel": {"price_range": 0.30},
        "Ammunition": {"price_range": 0.15},
    }

    inflation = 1.0

global_trade_good_status = {
    "Organics":         {"price_range": TRADE_GOODS_DATA["Organics"]["base_range"]},
    "Synthetics":       {"price_range": TRADE_GOODS_DATA["Synthetics"]["base_range"]},
    "Common Minerals":  {"price_range": TRADE_GOODS_DATA["Common Minerals"]["base_range"]},
    "Rare Minerals":    {"price_range": TRADE_GOODS_DATA["Rare Minerals"]["base_range"]},
    "Refined Minerals": {"price_range": TRADE_GOODS_DATA["Refined Minerals"]["base_range"]},
    "Essential Goods":  {"price_range": TRADE_GOODS_DATA["Essential Goods"]["base_range"]},
    "Medicine":         {"price_range": TRADE_GOODS_DATA["Medicine"]["base_range"]},
    "Vice Goods":       {"price_range": TRADE_GOODS_DATA["Vice Goods"]["base_range"]},
    "Technology Goods": {"price_range": TRADE_GOODS_DATA["Technology Goods"]["base_range"]},
    "Luxury Goods":     {"price_range": TRADE_GOODS_DATA["Luxury Goods"]["base_range"]},
    "Weapons":          {"price_range": TRADE_GOODS_DATA["Weapons"]["base_range"]},
    "Narcotics":        {"price_range": TRADE_GOODS_DATA["Narcotics"]["base_range"]},
    "Equipment Parts":  {"price_range": TRADE_GOODS_DATA["Equipment Parts"]["base_range"]},
    "Fuel":             {"price_range": TRADE_GOODS_DATA["Fuel"]["base_range"]},
    "Ammunition":       {"price_range": TRADE_GOODS_DATA["Ammunition"]["base_range"]},
}

def clamp(value, lower, upper):
    """
    Returns a value between lower and upper bounded
    :param value:
    :param lower:
    :param upper:
    :return:
    """
    return lower if value < lower else upper if value > upper else value


def map_range_max_clamped(value, in_min, in_max, out_min, out_max):
    """
    Maps a value from one range to another while clamping it to the input range.

    :param value: float - The input value to be mapped.
    :param in_min: float - The minimum value of the input range.
    :param in_max: float - The maximum value of the input range.
    :param out_min: float - The minimum value of the output range.
    :param out_max: float - The maximum value of the output range.
    :return: float - The mapped and clamped value in the output range.
    """
    # Clamp the value within the input range
    clamped_value = min(value, in_max) #clamp(value, in_min, in_max)

    # Normalize and map the value to the output range
    return out_min + (clamped_value - in_min) * (out_max - out_min) / (in_max - in_min)


def calculate_price_logistic(min_multiplier, max_multiplier, supply_ratio, buy_k=0.95, min_sell_discount=0.8,
                             max_sell_discount=0.98, sell_k=5):
    """
    Calculates the price point of a commodity based on a logistic supply-demand curve.
    Works well with high supply or negative values.

    :param min_multiplier: float - The lowest price multiplier at maximum surplus.
    :param max_multiplier: float - The highest price multiplier at maximum deficit.
    :param supply_ratio: Current Supply divided by Equilibrium Supply
    :param buy_k: float - Steepness of the curve (higher values create sharper price transitions).
    Recommend a value of 0.75
    :param min_sell_discount: float - The lowest discount (widest gap in surplus).
    :param max_sell_discount: float - The highest discount (smallest gap in deficit).
    :param sell_k: Similar to buy_k, tends to approach min and max_sell_discount when at low and high supply resp.
    Recommend a value of 5

    :return: float - The adjusted buy and sell price of the commodity.
    """

    buy_logistic_multiplier = min_multiplier + (max_multiplier - min_multiplier) / (
            1 + math.exp(-buy_k * (1 - supply_ratio)))

    sell_discount = min_sell_discount + (max_sell_discount - min_sell_discount) / (
            1 + math.exp(-sell_k * (1 - supply_ratio)))



    # print(sell_discount)
    return buy_logistic_multiplier, buy_logistic_multiplier * sell_discount


class TradeGoodStatus:
    def __init__(self, essential, legality, max_fluctuation, daily_fluctuation, buy_modifiers, sell_modifiers,
                 equilibrium_quantity, quantity):
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
        self.quantity = quantity

        # for display
        self.available_supply = 0
        self.average_buy_price = 0
        self.average_sell_price = 0
        self.min_buy_price = 0
        self.max_sell_price = 0

    def calculate_new_daily_fluctuation(self):
        self.daily_fluctuation = random.uniform(1 - self.max_fluctuation, 1 + self.max_fluctuation)

    def get_buy_modifier(self):
        return self.daily_fluctuation * (math.prod(self.buy_modifiers) if self.buy_modifiers else 1)

    def get_sell_modifier(self):
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
    # in respect to the operation
    # The market will still gradually adjust their prices over time.
    # Returns Deficit_Quantity, Major_Deficit_Quantity, Surplus_Quantity, Major_Surplus_Quantity
    return round(0.75 * equilibrium), round(0.2 * equilibrium), round(1.25 * equilibrium), round(2 * equilibrium)

def calculate_price_ranges(trade_difficulty):
    max_difficulty_penalty = 0.5  # maximum reduction in price ranges at hardest difficulty

    max_difficulty = 10
    min_difficulty = 1

    for trade_good in global_trade_good_status:
        # higher trade difficulties (value from 1 to 10) = lower profit margins
        base_range = global_trade_good_status[trade_good]["price_range"]

        # in essence, this is a sliding value from max_difficulty_penalty to 1.0 based on the trade difficulty selected
        global_trade_good_status[trade_good]["price_range"] = (base_range *
            (1.0 - ((trade_difficulty - min_difficulty) / (max_difficulty - min_difficulty)) * (1.0 - max_difficulty_penalty)))


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

    def get_all_order_listings_by_trade_good(self, trade_good, operation):
        order_listings = []
        if operation == "Buy":
            for ee in self.economy_entities:
                for bo in ee.buy_orders:
                    if trade_good == bo.trade_good:
                        order_listings.append(bo)
                        break
        elif operation == "Sell":
            for ee in self.economy_entities:
                for bo in ee.sell_orders:
                    if trade_good == bo.trade_good:
                        order_listings.append(bo)
                        break

        return order_listings

    def get_final_price_by_order(self, order_listing, trade_good, operation, min_buy_price=1000000):
        price_range = global_trade_good_status[trade_good]["price_range"]

        if operation == "Buy":
            return round(order_listing.get_price(self.trade_good_status[trade_good].get_buy_modifier(), 1 - price_range,
                                                 1 + price_range))
        elif operation == "Sell":
            price = round(order_listing.get_price(self.trade_good_status[trade_good].get_sell_modifier(), 1 - price_range,
                                        1 + price_range, 0.5, 1.5))
            #print(price)
            return min(price, min_buy_price)
        # maybe instead of 0.5-1.5 use the actual price points idk

    def get_final_price_by_value(self, price, trade_good, operation):
        if operation == "Buy":
            return round(price * self.trade_good_status[trade_good].get_buy_modifier())
        elif operation == "Sell":
            return round(price * self.trade_good_status[trade_good].get_sell_modifier())

    def summary_listing(self, trade_good, display=True):
        # average price - buying
        buy_weighted_average_price = 0
        buy_orders = self.get_all_order_listings_by_trade_good(trade_good, "Buy")
        buy_quantity_total = sum(order.quantity for order in buy_orders)
        self.trade_good_status[trade_good].quantity = buy_quantity_total

        for buy_order in buy_orders:
            # market share
            market_share = buy_order.quantity / buy_quantity_total
            # price
            buy_weighted_average_price = buy_weighted_average_price + (market_share * buy_order.get_price())

        buy_weighted_average_price = self.get_final_price_by_value(buy_weighted_average_price, trade_good, "Buy")

        # average price - selling
        sell_weighted_average_price = 0
        sell_orders = self.get_all_order_listings_by_trade_good(trade_good, "Sell")
        sell_quantity_total = sum(order.quantity for order in sell_orders)

        for sell_order in sell_orders:
            # market share
            market_share = sell_order.quantity / sell_quantity_total
            # price
            sell_weighted_average_price = sell_weighted_average_price + (market_share * sell_order.get_price())

        sell_weighted_average_price = self.get_final_price_by_value(sell_weighted_average_price, trade_good, "Sell")

        # Max and Min
        min_buy_order = min(buy_orders, key=lambda order: order.get_price())
        max_sell_order = max(sell_orders, key=lambda order: order.get_price())
        buy_minimum_price = self.get_final_price_by_order(min_buy_order, trade_good, "Buy")
        sell_maximum_price = self.get_final_price_by_order(max_sell_order, trade_good, "Sell")

        text = (
        (f"# {trade_good:<20} Available to buy: x{buy_quantity_total} at ~{round(buy_weighted_average_price)}cr --- "
         f"Available to sell x{sell_quantity_total} at ~{round(sell_weighted_average_price)}cr --- "
         f"Min/Buy at {buy_minimum_price}cr (x{min_buy_order.quantity}) --- "
         f"Max/Sell at {sell_maximum_price}cr (x{max_sell_order.quantity})"))

        return buy_orders, sell_orders, text

    def trade_good_listing(self, trade_good):
        if trade_good not in self.trade_good_status:
            print("N/A")
            return

        buy_orders, sell_orders, text = self.summary_listing(trade_good)
        # sell_orders.extend(sell_orders.copy()) # duplicates itself
        # buy_orders.extend(buy_orders.copy())  # duplicates itself
        print(
            "+---------------------------------------------------------------------------------------------------------------------------+")
        print(
            "|                                                      Technology Goods                                                     |")
        print(
            "+-------------------------------------------------------------+-------------------------------------------------------------+")
        print(
            "|                             Buy                             |                             Sell                            |")

        table_buy = PrettyTable(['Corporation', "Quantity", "Price", "Quality"])
        table_sell = PrettyTable(['Corporation', "Quantity", "Price", "Quality"])
        corp_name = "AAAAAAAAAAAAAAAAA"

        status = self.trade_good_status[trade_good]
        logistic_multiplier_buy, logistic_multiplier_sell = calculate_price_logistic(1 - status.price_range,
                                                                                     1 + status.price_range,
                                                                                     status.quantity,
                                                                                     status.equilibrium_quantity)
        # print(logistic_multiplier_buy, logistic_multiplier_sell)

        for order in buy_orders:
            table_buy.add_row(
                [f"{corp_name: ^30}", order.quantity, self.get_final_price_by_order(order, trade_good, "Buy"), "B"])

        for order in sell_orders:
            table_sell.add_row(
                [f"{corp_name: ^30}", order.quantity, self.get_final_price_by_order(order, trade_good, "Sell"), "B"])

        table_string = table_buy.get_string()
        table_string2 = table_sell.get_string()

        # Split tables into lines
        table_lines1 = table_string.splitlines()
        table_lines2 = table_string2.splitlines()

        # Find how many lines match in size
        common_length = min(len(table_lines1), len(table_lines2))

        # Remove the first character from matching lines only
        modified_table_lines2 = [
            line[1:] if i < common_length else line
            for i, line in enumerate(table_lines2)
        ]

        # Ensure both tables have the same number of lines by padding the shorter one
        max_lines = max(len(table_lines1), len(modified_table_lines2))

        # Find the length of the longest line for padding
        max_width1 = max(len(line) for line in table_lines1)
        max_width2 = max(len(line) for line in modified_table_lines2)

        # Pad the shorter table with empty rows to match the longer table
        while len(table_lines1) < max_lines:
            table_lines1.append(" " * (max_width1 - 1))
        while len(modified_table_lines2) < max_lines:
            modified_table_lines2.append(" " * max_width2)

        # Merge lines side by side
        final_table = "\n".join(f"{line1}{line2}" for line1, line2 in zip(table_lines1, modified_table_lines2))

        print(final_table)
        print("\n", text)

    def recalculate_prices(self):
        for trade_status in self.trade_good_status:
            self.trade_good_status[trade_status].calculate_new_daily_fluctuation()

    # show a summary of every trade good, 1 line each
    def quick_summary(self):
        return

    @staticmethod
    def generate_market(market_name, equilibrium, supply, market_score, price_range_index):
        trade_status1 = TradeGoodStatus("Non-Essential", "Legal", 0.025, 1,
                                        [], [], 500, 480)

        temp_trade_statuses = {}

        for trade_good in TRADE_GOODS_DATA:
            temp_trade_statuses[trade_good] = trade_status1


        temp = Market(market_name, market_score, [], temp_trade_statuses)
        ees = temp.generate_new_ees(equilibrium, supply, market_score, price_range_index, True)
        temp.economy_entities = ees
        return temp

    def generate_new_ees(self, equilibrium, supply, market_score, trade_difficulty=1, verbose=True):

        # TODO: create EEs for all of the remaining trade goods, figure out how to get names of corporations too.
        # for trade_good in TRADE_GOODS_DATA:

        tg = "Technology Goods"
        price_range = global_trade_good_status[tg]["price_range"]
        floor, ceil = 1 - price_range, 1 + price_range
        temp_status = TradeGoodStatus("Non-Essential", "Legal", 0.025, 1,
                                      [], [], equilibrium, supply)

        self.trade_good_status[tg] = temp_status

        # allocate supply for an amount of EEs
        # determine spread of prices across all EEs. 0.95x - 1.05x for base prices over 20, under 20 0.8x - 1.2x
        # this spread isn't related to price distributions on main.py as that's how much prices vary over multiple economies
        # create order listings for each EE by using the price spread
        # the price point depends on the quality where the random value tends to the range interval.
        ees = []
        qualities = ['D', 'C', 'B', 'A']

        # available supply is what the market offers to export to avoid a player induced deficit by not making available
        # everything to purchase. If Equilibrium is 100, you won't be able to buy enough to cause supply go below
        # 0.75x - 75 units. Meaning the player can only buy from 0.75 ratio and above. However, the price calculations
        # still use of the total supply existing on the market
        internal_supply = True
        available_supply = supply - bracketed_pricing(equilibrium)[0] if internal_supply else supply
        buy_goods = normalrandom.trade_good_distribution(available_supply, 7)

        self.trade_good_status[tg].available_supply = available_supply

        names = ['Lord Technologies', 'Infinity Inc.', 'Celestial Industries', 'Nillaik Systems Ltd.',
                 'Voidware Devices',
                 'Inilai Electronics', 'Interstellar Circuits']

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
        #print(sell_ratio)


        # BUY ORDERS
        buy_final_prices = []
        quality_modifiers = []
        buy_orders = []
        # print(quality_distribution)
        for i in range(7):
            quality_modifier = get_quality_price_multiplier(60, quality_distribution[i])
            quality_modifiers.append(quality_modifier)
            price_point = buy_price * quality_modifier * market_score
            # print(quality_modifier)

            # cap price point to max_multiplier from trade status

            buy_order = OrderListing(tg, price_point, buy_goods[i], quality_distribution[i])
            buy_orders.append(buy_order)
            ee = EconomyEntity("Enterprise", names[i], [buy_order], [])
            # print(buy_order.get_price())
            ees.append(ee)
            buy_final_prices.append(self.get_final_price_by_order(buy_order, tg, "Buy"))

        # SELL ORDERS - create sell orders by determining the sell quantity
        # the total quantity for sell orders is determined by 2equilibrium_quantity - quantity
        # the spread is more smoothed out to give the largest producers still a fair amount with spread = 0.4
        sell_goods = normalrandom.trade_good_distribution(2 * equilibrium - supply, 7, 0.4)
        sell_goods.reverse()
        sell_orders = []
        # print(sell_goods)

        # get the minimum buying price to then establish a maximum selling price
        max_sell_final_price = min(buy_final_prices) - 1

        if verbose:
            print(buy_price * market_score, sell_price * market_score)
            print(f"Min:{max_sell_final_price}")
        #print(60 * market_score * buy_price, 60 * market_score * sell_price)
        sell_final_prices = []


        for i in range(7):
            #quality_modifier = get_quality_price_multiplier(60, quality_distribution[i])

            price_point = sell_price * quality_modifiers[i] * market_score

            sell_order = OrderListing(tg, price_point, sell_goods[i], quality_distribution[i])
            sell_orders.append(sell_order)
            sell_final_prices.append(self.get_final_price_by_order(sell_order, tg, "Sell", max_sell_final_price))
             #print(sell_order.get_price(1, floor, ceil))
            ees[i].sell_orders.append(sell_order)

            #print(price_point)

            if verbose:
                print(f"{ees[i].name:>25} - Buy (x{buy_orders[i].quantity:<5}) at {buy_final_prices[i]:>4}cr | "
                  f"Sell (x{sell_order.quantity:<5}) at {sell_final_prices[i]:>4}cr - Q:{buy_orders[i].quality}")

        if 0.75 < ratio < 1.25:
            situation = "Balanced"
        elif ratio <= 0.75:
            situation = "Deficit"
        else:
            situation = "Surplus"

        if ratio <= 0.2 or ratio >= 2:
            situation = "Major " + situation

        if verbose:
            print(f"Situation - {situation}")
            print(f"Breakoffs - {bracketed_pricing(equilibrium)}")
            print(f"Available for export: {available_supply} | Internal supply: {bracketed_pricing(equilibrium)[0] - abs(min(0, available_supply))} | Total: {supply}")

            buy_stuff = list(zip(buy_final_prices, buy_goods))
            sell_stuff = list(zip(sell_final_prices, sell_goods))

            # Filter out invalid (zero-quantity) orders for correct total quantity calculation
            valid_buy_orders = [(p, q) for p, q in buy_stuff if q > 0]
            valid_sell_orders = [(p, q) for p, q in sell_stuff if q > 0]

            # Calculate total valid quantities
            buy_total_quantity = sum(q for _, q in valid_buy_orders) if valid_buy_orders else 1
            sell_total_quantity = sum(q for _, q in valid_sell_orders) if valid_sell_orders else 1

            # Calculate weighted average price - buying
            buy_weighted_average_price = sum(
                (q / buy_total_quantity) * p for p, q in valid_buy_orders) if valid_buy_orders else 0
            buy_weighted_average_price = str(round(buy_weighted_average_price)) + "cr"

            # Calculate weighted average price - selling
            sell_weighted_average_price = sum(
                (q / sell_total_quantity) * p for p, q in valid_sell_orders) if valid_sell_orders else 0
            sell_weighted_average_price = str(round(sell_weighted_average_price)) + "cr"

            # Finding min buy price and max sell price, ignoring zero-quantity orders
            valid_buy_orders = [(p, q) for p, q in buy_stuff if q > 0]
            valid_sell_orders = [(p, q) for p, q in sell_stuff if q > 0]

            if valid_buy_orders:
                min_buy_price = min(valid_buy_orders)[0]
                min_buy_quantity = sum(q for p, q in valid_buy_orders if p == min_buy_price)
            else:
                min_buy_price, min_buy_quantity = min(buy_stuff)[0], 0

            if valid_sell_orders:
                max_sell_price = max(valid_sell_orders)[0]
                max_sell_quantity = sum(q for p, q in valid_sell_orders if p == max_sell_price)
            else:
                max_sell_price, max_sell_quantity = max(sell_stuff)[0], 0

            min_buy_price = str(min_buy_price) + "cr"
            max_sell_price = str(max_sell_price) + "cr"

            print(f"Average prices: {buy_weighted_average_price}/{sell_weighted_average_price} "
                  f"| Min buy: {min_buy_price} (x{min_buy_quantity}) | Max sell: {max_sell_price} (x{max_sell_quantity})")






        return ees


class EconomyEntity:
    def __init__(self, ee_type, name, buy_orders, sell_orders):
        """
        Abbreviated as "ee"

        :param name: string
        :param buy_orders: list of OrderListings to buy
        :param sell_orders: list of OrderListing to sell
        """
        self.type = ee_type
        self.name = name
        self.buy_orders = buy_orders
        self.sell_orders = sell_orders

    def __str__(self):
        return f"{self.name} - [{type}] : Buy:{self.buy_orders[0].get_price()} | Sell:{self.sell_orders[0].get_price()}"


class OrderListing:
    def __init__(self, trade_good, price_point, quantity, quality='B'):
        """
        Only one order listing per trade good to sell and one to buy for each EconomyEntity
        :param trade_good:
        :param price_point:
        :param quantity:
        """
        self.trade_good = trade_good
        self.price_point = price_point
        self.quantity = quantity
        self.quality = quality

    def get_price(self, modifiers=1, out_min=0.55, out_max=1.45, in_min=0.5, in_max=1.5):
        return inflation * TRADE_GOODS_DATA[self.trade_good]["base_price"] * self.price_point * modifiers
                #experimenting without clamping any values since logistic function by itself kinda does this
                #map_range_max_clamped(, in_min, in_max, out_min, out_max))\

"""
ol1 = OrderListing("Technology Goods", 0.975, 100)
ol2 = OrderListing("Technology Goods", 1.025, 200)
ol3 = OrderListing("Technology Goods", 1.0, 50)
ol4 = OrderListing("Technology Goods", 0.99, 30)
ol5 = OrderListing("Technology Goods", 1.01, 100)

sol1 = OrderListing("Technology Goods", 0.975 / 1.1, 50)
sol2 = OrderListing("Technology Goods", 1.025 / 1.1, 30)
sol3 = OrderListing("Technology Goods", 1.0 / 1.1, 80)
sol4 = OrderListing("Technology Goods", 0.99 / 1.1, 40)
sol5 = OrderListing("Technology Goods", 1.01 / 1.1, 60)

ee1 = EconomyEntity("Enterprise",
                    "Celestial Industries",
                    [ol1], [sol1])

ee2 = EconomyEntity("Enterprise",
                    "Lord Technologies",
                    [ol2], [sol2])

ee3 = EconomyEntity("Enterprise",
                    "Titan Industries",
                    [ol3], [sol3])

ee4 = EconomyEntity("Enterprise",
                    "Hope Systems Ltd.",
                    [ol4], [sol4])

ee5 = EconomyEntity("Enterprise",
                    "Hyperion Devices",
                    [ol5], [sol5])


trade_statuses = {
    trade_goods[0]: trade_status1,
    trade_goods[1]: trade_status1,
    trade_goods[2]: trade_status1,
    trade_goods[3]: trade_status1,
    trade_goods[4]: trade_status1,
    trade_goods[5]: trade_status1,
    trade_goods[6]: trade_status1,
    trade_goods[7]: trade_status1,
    trade_goods[8]: trade_status1,
    trade_goods[9]: trade_status1,
    trade_goods[10]: trade_status1,
    trade_goods[11]: trade_status1,
    trade_goods[12]: trade_status1,
    trade_goods[13]: trade_status1,
    trade_goods[14]: trade_status1,
}

#market = Market("Planet A", 1000, [ee1, ee2, ee3, ee4, ee5], trade_statuses)

#market.generate_new_ees(False)

market.trade_good_listing("Technology Goods")
player_input = input("w to wait, q to quit :> ")
while player_input.lower() != "q" or player_input.lower() != "quit" or player_input.lower() != "exit":
    if player_input.lower() == "w" or player_input.lower() == "wait":
        #clear screen, calculate new prices and display
        #os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" * 10)
        market.recalculate_prices()
        market.trade_good_listing("Technology Goods")
        print(market.trade_good_status["Technology Goods"].daily_fluctuation)
        player_input = input("w to wait, q to quit :> ")
#market.summary_listing("Technology Goods")
"""