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

    if operation in ["s", "b", "a", "r", "bl", "sl", "w", "al", "rl", "wl", "help", "t", "h", "l"]:
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
          "ab [quantity] [maximum price : optional] [minimum quality : optional] - Attempts to auto buy the selected quantity of goods starting by price ascending. Prioritizes higher quality goods when there's a price tie.\n"
          "Can buy from multiple corporations. minimum quality default is 'C'. Will stop when quantity is reached or if there are no quantities available or if there are no goods with the minimum quality\n"
          "as [quantity] [minimum price : optional] - Similar to auto buy, will attempt to auto sell all goods starting by price descending and prioritize lower quality goods to where it can be sold\n")


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
            "Enter trade difficulty (1-10), market size (500-3000) and development score (0.9-1.1) separated by spaces\nOr press Enter for default values (1 1000 1.0)\n> ")
        setup_input2 = setup_input.strip().split()
        if not setup_input2:
            trade_difficulty, market_size, development_score = 1, 1000, 1.0
            break

        try:
            trade_difficulty, market_size, development_score = setup_input2

            trade_difficulty = clamp(int(trade_difficulty), 1, 10)
            market_size = clamp(int(market_size), 500, 3000)
            development_score = clamp(float(development_score), 0.9, 1.1)
            break
        except ValueError:
            print("Invalid input, enter something like '2 0.9' or press Enter for default values (1 1.0)")

    simulation_status.trade_difficulty = trade_difficulty
    SimulationStatus().calculate_price_ranges(trade_difficulty)

    market_names = ["Earth", "Phedok", "Gaaldok", "Eipentak", "Ramgatroo"]
    markets = []

    political_systems = ["Democracy", "Republic", "Dictatorship", "Monarchy", "Anarchy"]
    development_types = ["Agrarian", "Mixed", "Industrial"]

    tg = "Technology Goods"
    political_system = "Democracy"
    development_type = "Mixed"
    print(market_size)


    market = Market.generate_market("Planet", market_size, development_score, political_system, development_type)

    for name in market_names:
        markets.append(Market.generate_market(name, market_size, development_score, political_system, development_type))

    markets.append(market)

    user = Actor(10000)
    market.summary_listing(tg)
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
                print(f"You bought {item.total_quantity} {tg} from {item.producer.name} for a total of {item.total_cost}cr!")
                command, params = parse_command()
                continue

            brackets = item.breakdown_prices

            for q, p in brackets:
                print(f"You bought {q} {tg} at {p}cr each")

            print(f"Totaling {item.total_quantity} {tg} from {item.producer.name} for {item.total_cost}cr!")


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

            user.remove_item(item)
            if len(item.breakdown_prices) == 1:
                print(f"You sold {item.total_quantity} {tg} for a total of {item.total_cost}cr!")
                command, params = parse_command()
                continue

            for q, p in item.breakdown_prices:
                print(f"You sold {q} {tg} at {p}cr each")

            print(f"Totaling {item.total_quantity} {tg} for {item.total_cost}cr!")

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

        if command == "h":
            market.summary_listing(tg)

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

