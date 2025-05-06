import random

from market import *
from math2 import clamp
from collections import defaultdict

def regroup_trade_good_statuses(list_of_markets):
    """
    :param list_of_markets: list of Market instances, each with a .trade_good_status dict {trade_good_name: MarketGoodStatus}
    :return: dict {trade_good_name: list of MarketGoodStatus across all markets}
    """
    regrouped = defaultdict(list)

    for m in list_of_markets:
        for t, status in m.trade_good_status.items():
            regrouped[t].append(status)

    return dict(regrouped)

def parse_command():
    processed_input = input("> ").strip().lower()
    groups = processed_input.split()

    if not groups:
        return None, []

    operation = groups[0]
    parameters = groups[1:]

    parameters = [int(param) if param.isdigit() else param for param in parameters]

    if operation in ["s", "b", "a", "r", "bl", "sl", "w", "al", "rl", "wl", "help", "t", "h", "l", "m", "i", "f"]:
        return operation, parameters

    if operation in ["q", "quit", "exit"]:
        return "q", []  # e.g., ('w', None) or ('quit', None)

    return None, None  # Invalid input

def display_help():
    print("\n"
        "Main Commands\n"
        "h - home screen, show summary listing for all trade goods on the market\n"
        "t [trade good index] - to switch to another trade good\n"
        "help - show this command list\n"
        "q - quit\n"
        "w [number of days: optional] - skip time to see changes in price\n\n"
        "Operation commands\n"
        "l - show detailed listing of the selected trade good. Can be appended to the first word of a command to execute both commands like bl or sl or abl \n"
        "b [corporation index] [quantity] - to buy\n"
        "s [corporation index] [quantity] - to sell\n"
        "a [corporation index] [quantity] - debug command, to add goods to a corporation\n"
        "r [quantity] - debug command, to remove goods from the market\n"
        "i - show inventory\n"
        "m [market_id : optional] - display existing markets and switch to another market if index is provided\n"
        "f [profit margin : optional] [supply share : optional] [total profit : optional] - find profitable trades with the specified parameters, e.g. f 0.2 0.1 1000\n")

          #"ab [quantity] [maximum price : optional] [minimum quality : optional] - Attempts to auto buy the selected quantity of goods starting by price ascending. Prioritizes higher quality goods when there's a price tie.\n"
          #"Can buy from multiple corporations. minimum quality default is 'C'. Will stop when quantity is reached or if there are no quantities available or if there are no goods with the minimum quality\n"
          #"as [quantity] [minimum price : optional] - Similar to auto buy, will attempt to auto sell all goods starting by price descending and prioritize lower quality goods to where it can be sold\n")


def find_profitable_trades(markets, minimum_margin=0.0, minimum_share=0.0, minimum_profit=0, verbose=True):
    profitable_trades = []
    total = 0

    for trade_good in TRADE_GOODS_DATA:
        for i, sell_market in enumerate(markets):
            status_sell = sell_market.trade_good_status[trade_good]
            sell_order = sell_market.sell_order.get(trade_good)
            if not sell_order:
                continue
            sell_price = sell_order.calculated_price

            for j, buy_market in enumerate(markets):
                status_buy = buy_market.trade_good_status[trade_good]

                if i == j:
                    continue  # skip same market


                buy_orders = buy_market.buy_orders.get(trade_good, [])

                if status_buy.available_supply <= 0:
                    total += len(buy_orders)
                    continue  # skip empty markets

                for buy_order in buy_orders:
                    total += 1
                    buy_price = buy_order.calculated_price
                    profit = sell_price - buy_price

                    if profit > 0:
                        margin = profit / buy_price
                        share = buy_order.quantity / status_buy.available_supply
                        total_profit = buy_order.quantity * profit
                        trade = {
                            "buy_market": buy_market.name,
                            "trade_good": trade_good,
                            "buy_price": buy_price,
                            "quantity": buy_order.quantity,
                            "sell_market": sell_market.name,
                            "sell_price": sell_price,
                            "profit_per_unit": profit,
                            "total_profit": total_profit,
                            #"margin": f"{round(margin * 100, 1)}%"
                            "margin": margin
                        }
                        if margin > minimum_margin and share > minimum_share and total_profit > minimum_profit:
                            if verbose:
                                print(trade)
                            profitable_trades.append(trade)

    average_profit = sum([trade["margin"] for trade in profitable_trades]) / len(profitable_trades)
    print(f"Displaying {len(profitable_trades)} - ({round(len(profitable_trades) / total * 100, 1)}%) profitable trades out of {total} total at the requested parameters ({minimum_margin} {minimum_share} {minimum_profit}), average profits: {round(average_profit * 100, 1)}")
    return profitable_trades


if __name__ == "__main__":
    simulation_status = SimulationStatus()
    """Singleton test
    print(simulation_status.inflation)
    simulation_status2 = SimulationStatus()
    simulation_status2.inflation = 2.0
    print(simulation_status.inflation)
    #"""

    while True:
        setup_input = input(
            "Enter trade difficulty (1-10) and an additional amount of markets to generate (don't recommend more than 50)\n> ")
        setup_input2 = setup_input.strip().split()
        if not setup_input2:
            trade_difficulty, additional_markets = 1, 5
            break

        try:
            trade_difficulty, additional_markets = setup_input2

            trade_difficulty = clamp(int(trade_difficulty), 1, 10)
            additional_markets = clamp(int(additional_markets), 0, 1000)
            break
        except ValueError:
            print("Invalid input, enter something like '2 5' or press Enter for default values (1 5)")

    simulation_status.trade_difficulty = trade_difficulty
    SimulationStatus().calculate_price_ranges(trade_difficulty)

    markets = []

    min_development, max_development = LOWER_DEVELOPMENT_SCORE, UPPER_DEVELOPMENT_SCORE
    min_size, max_size = 500, 3000
    political_systems = ["Democracy", "Republic", "Dictatorship", "Monarchy", "Anarchy", "Theocracy"]
    development_types = ["Agrarian", "Mixed", "Industrial"]
    races = ["Human", "Peleng", "Gaalian", "Faeyan", "Maloq"]

    tg = "Technology Goods"

    market = Market.generate_market("Earth", "Human", 1000, 1.0, "Democracy", "Industrial")
    markets.append(Market.generate_market("Phedok", "Peleng", 1100, 0.9, "Republic", "Mixed"))
    markets.append(Market.generate_market("Gaaldok", "Gaalian", 1200, 1.1, "Monarchy", "Industrial"))
    markets.append(Market.generate_market("Eypentak", "Faeyan", 1100, 1.2, "Republic", "Industrial"))
    markets.append(Market.generate_market("Ramgatru", "Maloq", 1100, 0.8, "Dictatorship", "Mixed"))

    markets.append(market)

    #additional_markets = 200
    for i in range(additional_markets):
        markets.append(Market.generate_market(f"Market-{i}", random.choice(races),
                                              random.randint(min_size, max_size),
                                              random.uniform(min_development, max_development),
                                              random.choice(political_systems),
                                              random.choice(development_types)))

    user = Actor(10000)
    market.market_listing(tg)
    print("\nType help for complete list of commands\n")
    command, params = parse_command()

    while command != "q" :

        if command is None:
            print("Invalid command. Type h for complete command list")

        if command in ["b", "bl"]:
            if len(params) < 2:
                print(f"Usage: b{'l' if command in ["bl", "sl"] else ''} [producer index] [quantity]")
                command, params = parse_command()
                continue

            producer_index, quantity = int(params[0]) - 1, int(params[1])

            if not (0 <= producer_index < len(market.buy_orders[tg]) + 1 and quantity > 0):
                print(f"Input a valid corporation index number 1 - {len(market.buy_orders[tg])} and a positive quantity number")
                command, params = parse_command()
                continue

            # if buy, add item to actor and merge quantities if already exists
            item = market.buy(tg, producer_index, quantity)

            if item.total_quantity == -1:
                print("Can only buy from producers with a positive amount")
                command, params = parse_command()
                continue

            user.add_item(item)
            if len(item.breakdown_prices) == 1:
                print(f"You bought {item.total_quantity} {tg} from {item.producer.name} for a total of {item.total_value}cr!")
                command, params = parse_command()
                continue

            brackets = item.breakdown_prices

            for q, p in brackets:
                print(f"You bought {q} {tg} at {p}cr each")

            user.money -= item.total_value
            print(f"Totaling {item.total_quantity} {tg} from {item.producer.name} for {item.total_value}cr! Your money: {user.money}cr")


        if command in ["s", "sl"]:
            if len(params) < 2:
                print(f"Usage: s{'l' if command in ["bl", "sl"] else ''} [item index] [quantity]")
                command, params = parse_command()
                continue

            item_index, quantity = int(params[0]) - 1, int(params[1])

            if not (0 <= item_index < len(user.items) and quantity > 0):
                print(f"Input a valid item index number 1 - {len(user.items)} and a positive quantity number")
                command, params = parse_command()
                continue

            if quantity < 1:
                print(f"Can only sell a positive amount")
                command, params = parse_command()
                continue

            sell_amount = market.sell_order[tg].quantity
            if sell_amount <= 0:
                print(f"Market refuses to accept any more {tg}")
                command, params = parse_command()
                continue

            sell_amount = min(sell_amount, quantity)

            item = user.items[item_index]
            item = market.sell(tg, item, sell_amount) # returns the amount of items that were sold

            user.remove_item(item) # TODO: market should only sell if this doesn't fail as this executes anyway
            if len(item.breakdown_prices) == 1:
                print(f"You sold {item.total_quantity} {tg} for a total of {item.total_value}cr!")
                command, params = parse_command()
                continue

            for q, p in item.breakdown_prices:
                print(f"You sold {q} {tg} at {p}cr each")

            user.money += item.total_value
            print(f"Totaling {item.total_quantity} {tg} for {item.total_value}cr! Your money: {user.money}cr")

        if command in ["a", "al"]:
            if len(params) >= 2 and 0 < int(params[0]) < len(market.buy_orders[tg]) + 1 and int(params[1] > 0):
                added = market.add_goods(tg, params[0] - 1, params[1])
                print(f"Added {added} {tg} to the market!")

        if command in ["r", "rl"]:
            if len(params) >= 1 and int(params[0] > 0):
                removed = market.remove_goods(tg, params[0])
                print(f"Removed {removed} {tg} from the market!")

        if command in ["ab", "as"]:
            print("Not implemented.")

        if command == "f":
            margin = 0.2
            minimum_share = 0.1
            total_profit = 500
            if len(params) > 0:
                margin = float(params[0])

            if len(params) > 1:
                minimum_share = float(params[1])

            if len(params) > 2:
                total_profit = int(params[2])

            find_profitable_trades(markets, margin, minimum_share, total_profit, True)

        if command == "h":
            market.market_listing(tg)

        if command == "m":
            if not params:
                for i, market in enumerate(markets):
                    print(f"{i+1} - {market.short_listing()}")
            else:
                market_index = int(params[0]) - 1

                if not (0 <= market_index < len(markets)):
                    print("Need valid market index")
                    command, params = parse_command()
                    continue

                market = markets[market_index]
                market.market_listing(tg)

        if command == "i":
            print(f"Money: {user.money}cr")
            print("\nTrade Goods")
            for i, item in enumerate(user.items):
                print(
                    f"{i + 1}. - x{item.total_quantity:<5} {item.trade_good} at {round(item.total_value / item.total_quantity)}cr manufactured by {item.producer.name}")

        if command == "w":
            days = SimulationStatus().days_elapsed
            if params:
                SimulationStatus().set_to_day(SimulationStatus().days_elapsed + params[0])
            else:
                SimulationStatus().skip_day()

            statuses = regroup_trade_good_statuses(markets)
            days = SimulationStatus().days_elapsed - days

            # for market in markets:
            market.balance_quantities_sell()
            for trade_good in TRADE_GOODS_DATA:
                SimulationStatus().global_good_status[trade_good].calculate_daily_fluctuation(statuses[trade_good])
                print(f"New fluctuation for {trade_good} - {SimulationStatus().global_good_status[trade_good].current_fluctuation}")

                market.balance_quantities(trade_good)
                market.drift_prices(trade_good)
                market.recalculate_prices(trade_good, "", False)
            print(f"Waited {days} day{'s' if days > 1 else ''}, new inflation {SimulationStatus().inflation}")

        if command == "t":
            goods = list(market.buy_orders.keys())
            index = params[0] - 1
            if 0 <= index < len(goods):
                tg = goods[index]
                print(f"Switched operating to {goods[index]}")
            else:
                print(f"Invalid trade good index, try 1 - {len(goods)}")

        if command == "help":
            display_help()

        if command is not None and command[-1] == "l":
            market.detailed_listing(tg, user.items)

        command, params = parse_command()

