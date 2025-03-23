
from prettytable import PrettyTable







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