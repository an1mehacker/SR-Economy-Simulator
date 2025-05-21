import time
import tracemalloc
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

def wait():
    start_time = time.time()
    statuses = regroup_trade_good_statuses(markets)
    for trade_good in TRADE_GOODS_DATA:
        SimulationStatus().global_good_status[trade_good].calculate_daily_fluctuation(statuses[trade_good])
    for m in markets:
        m.balance_quantities_sell()
        if m == market:
            m.consumption_production(True)
        else:
            m.consumption_production()
        for trade_good in TRADE_GOODS_DATA:
            m.balance_quantities(trade_good)
            m.drift_prices(trade_good)
            # recalculating prices should be the last thing to do
            m.recalculate_prices(trade_good, "", False)
            m.update_available_supply(trade_good)

    elapsed = time.time() - start_time
    return elapsed

def parse_command():
    processed_input = input("> ").strip().lower()
    groups = processed_input.split()

    if not groups:
        return None, []

    operation = groups[0]
    parameters = groups[1:]

    parameters = [int(param) if param.isdigit() else param for param in parameters]

    if operation in ["s", "b", "a", "r", "bl", "sl", "w", "al", "rl", "wl", "help", "t", "h", "l", "m", "i", "f", "dp", "do", "set"]:
        return operation, parameters

    if operation in ["q", "quit", "exit"]:
        return "q", []  # e.g., ('w', None) or ('quit', None)

    return None, None  # Invalid input

def display_help():
    print("\n"
        "Main Commands\n"
        "f [profit margin : optional] [supply share : optional] [total profit : optional] - find profitable trades with the specified parameters, e.g. f 0.2 0.1 1000\n"
        "m [market_id : optional] - display existing markets and switch to another market if index is provided\n"
        "h - home screen, show summary listing for all trade goods on the market\n"
        "t [trade good index] - to switch to another trade good\n"
        "help - show this command list\n"
        "q - quit\n"
        "w [number of days: optional] - skip time to see changes in price\n\n"
        "Operation commands\n"
        "l - show detailed listing of the selected trade good. Can be appended to the first word of a command to execute both commands like bl or sl or abl \n"
        "b [producer index] [quantity] - to buy\n"
        "s [producer index] [quantity] - to sell\n"
        "a [producer index] [quantity] - debug command, to add goods to a corporation\n"
        "r [quantity] - debug command, to remove goods from the market\n"
        "i - show inventory\n")

          #"ab [quantity] [maximum price : optional] [minimum quality : optional] - Attempts to auto buy the selected quantity of goods starting by price ascending. Prioritizes higher quality goods when there's a price tie.\n"
          #"Can buy from multiple corporations. minimum quality default is 'C'. Will stop when quantity is reached or if there are no quantities available or if there are no goods with the minimum quality\n"
          #"as [quantity] [minimum price : optional] - Similar to auto buy, will attempt to auto sell all goods starting by price descending and prioritize lower quality goods to where it can be sold\n")


def find_profitable_trades(markets, minimum_margin=0.0, minimum_share=0.0, minimum_profit=0, filtered_tg=-1,verbose=True):
    profitable_trades = []
    total = 0

    trade_index = 0
    # expensive operation especially when the amount of markets is large
    for trade_good in TRADE_GOODS_DATA:

        if filtered_tg != -1 and filtered_tg != trade_index:
            trade_index += 1
            continue

        trade_index += 1
        for i, sell_market in enumerate(markets):
            sell_order = sell_market.sell_order.get(trade_good)
            if not sell_order or sell_order.quantity <= 0:
                continue
            sell_price = sell_order.calculated_price

            for j, buy_market in enumerate(markets):
                status_buy = buy_market.trade_good_status[trade_good]

                if i == j:
                    continue  # skip same market


                buy_orders = buy_market.buy_orders.get(trade_good, [])

                if status_buy.available_supply <= 0:
                    total += 1
                    continue  # skip empty markets

                valid_buy_orders = []
                profits = []
                for buy_order in buy_orders:
                    buy_price = buy_order.calculated_price
                    profit = sell_price - buy_price

                    if profit > 0 and buy_order.quantity > 0:
                        valid_buy_orders.append(buy_order)
                        profits.append(profit)

                if valid_buy_orders:
                    total += 1

                    # Calculate total valid quantities
                    buy_total_quantity = sum(order.quantity for order in valid_buy_orders)

                    # Calculate weighted average price - buying
                    buy_weighted_margins = 0
                    total_profit = 0
                    buy_weighted_price = 0
                    profit_per_unit = 0
                    for k, order in enumerate(valid_buy_orders):
                        buy_weighted_margins += profits[k] / order.calculated_price * (order.quantity / buy_total_quantity)
                        buy_weighted_price += order.calculated_price * (order.quantity / buy_total_quantity)
                        profit_per_unit += profits[k] * (order.quantity / buy_total_quantity)
                        total_profit += order.quantity * profits[k]


                    margin = round(profit_per_unit / buy_weighted_price, 3)
                    share = buy_total_quantity / status_buy.available_supply

                    trade = {
                        "buy_market": buy_market.name,
                        "trade_good": trade_good,
                        "buy_price": round(buy_weighted_price),
                        "quantity": buy_total_quantity,
                        "sell_market": sell_market.name,
                        "sell_price": sell_price,
                        "profit_per_unit": round(profit_per_unit),
                        "total_profit": total_profit,
                        "margin": margin
                    }
                    if margin > minimum_margin and share > minimum_share and total_profit > minimum_profit:
                        profitable_trades.append(trade)

    max_trades = 100
    if verbose:
        profitable_trades = sorted(profitable_trades, key=lambda t: t["margin"], reverse=False)
        for trade in profitable_trades[-max_trades:]:
            print(
                f"{trade['trade_good']:<20}: Buy @{trade['buy_market']:<12} {trade['buy_price']:>4}cr → "
                f"Sell @{trade['sell_market']:<12} {trade['sell_price']:>4}cr | Qty: {trade['quantity']:>5} | "
                f"Profit: {trade['total_profit']:>7}cr | Margin: {round(trade['margin'] * 100, 1)}%")


    if len(profitable_trades) > 0:
        average_profit = sum([trade["margin"] for trade in profitable_trades]) / len(profitable_trades)
        print(f"Displaying {min(max_trades, len(profitable_trades))} - profitable trades out of {total} total "
              f"({round(len(profitable_trades) / total * 100, 1)}%) at the requested parameters ({minimum_margin} "
              f"{minimum_share} {minimum_profit}), average profits: {round(average_profit * 100, 1)}%")
    else:
        print(f"Could not find any profitable trades under requested parameters ({minimum_margin} {minimum_share} {minimum_profit})")
    return profitable_trades


if __name__ == "__main__":
    tracemalloc.start()
    simulation_status = SimulationStatus()

    while True:
        setup_input = input(
            "Enter trade difficulty (1-10) and an additional amount of markets to generate (don't recommend more than 300)\n> ")
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

    current, peak = tracemalloc.get_traced_memory()
    print(f"Current memory usage: {current / 1024 / 1024:.1f} MB")
    print(f"Peak usage: {peak / 1024 / 1024:.1f} MB")
    tracemalloc.stop()
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
            user.money -= item.total_value
            if len(item.breakdown_prices) == 1:
                print(f"You bought {item.total_quantity} {tg} from {item.producer.name} for a total of {item.total_value}cr!")
                command, params = parse_command()
                continue

            brackets = item.breakdown_prices

            for q, p in brackets:
                print(f"You bought {q} {tg} at {p}cr each")

            print(f"Totaling {item.total_quantity} {tg} from {item.producer.name} for {item.total_value}cr! Your money: {user.money}cr")


        if command in ["s", "sl"]:
            if len(params) < 2:
                print(f"Usage: s{'l' if command in ["bl", "sl"] else ''} [item index] [quantity]")
                command, params = parse_command()
                continue

            item_index, quantity = int(params[0]) - 1, int(params[1])

            amount_of_items = user.get_amount_of_items(tg)
            if not (0 <= item_index < amount_of_items and quantity > 0):
                print(f"Input a valid item index number 1 - {amount_of_items} and a positive quantity number")
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

            found_item = [item for item in user.items if item.trade_good == tg][item_index]

            sell_amount = min(sell_amount, quantity)

            item_index = user.find_item_index(found_item)
            item = user.items[item_index]
            old_cost = item.total_value

            item = market.sell(tg, item, sell_amount) # returns the amount of items that were sold
            revenue = item.total_value

            user.remove_item(item) # TODO: market should only sell if this doesn't fail as this executes anyway
            user.money += item.total_value
            if len(item.breakdown_prices) == 1:
                print(f"You sold {item.total_quantity} {tg} for a total of {item.total_value}cr! "
                      f"Profit: {revenue - old_cost}cr - Margins: {round(100 * (revenue - old_cost) / old_cost, 1)}%"
                      f"\nYour money: {user.money}cr")
                command, params = parse_command()
                continue

            for q, p in item.breakdown_prices:
                print(f"You sold {q} {tg} at {p}cr each")

            print(f"Totaling {item.total_quantity} {tg} for {item.total_value}cr! "
                  f"Profit: {revenue - old_cost}cr - Margins: {round(100 * (revenue - old_cost) / old_cost, 1)}%"
                  f"\nYour money: {user.money}cr")

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
            total_gain = 500
            filtered_tg = -1
            if len(params) > 0:
                margin = float(params[0])

            if len(params) > 1:
                minimum_share = float(params[1])

            if len(params) > 2:
                total_gain = int(params[2])

            if len(params) > 3:
                filtered_tg = int(params[3]) - 1 if 0 < int(params[3]) <= len(TRADE_GOODS_DATA.keys()) else -1

            find_profitable_trades(markets, margin, minimum_share, total_gain, filtered_tg,True)

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
            elapsed_time = 0
            if params:
                for _ in range(int(params[0])):
                    SimulationStatus().skip_day()
                    elapsed_time += wait()
            else:
                SimulationStatus().skip_day()
                elapsed_time += wait()

            days = SimulationStatus().days_elapsed - days
            print(f"Waited {days} day{'s' if days > 1 else ''}, new inflation {SimulationStatus().inflation}, operation took {elapsed_time:.2f}s")

        if command == "t":
            if len(params) < 1:
                print(f"Usage: t [trade good index]")
                command, params = parse_command()
                continue

            goods = list(market.buy_orders.keys())
            index = params[0] - 1
            if 0 <= index < len(goods):
                tg = goods[index]
                print(f"Switched operating to {goods[index]}")
            else:
                print(f"Invalid trade good index, try 1 - {len(goods)}")

        if command == "do":
            # Debug producer
            order_index = int(params[0])
            order = market.buy_orders[tg][order_index]
            print(order)

        if command == "dp":
            # Debug prices
            ratio = market.trade_good_status[tg].total_supply / market.trade_good_status[tg].equilibrium_quantity
            market.simulate_buy_price(tg, ratio, 0)
            market.simulate_sell_price(tg, ratio, Item(tg, 0, [], '', ""))

        if command == "set":
            if not params or len(params) < 2:
                print(f"Usage: set [eq/sup/bp/sp] [value]")
                command, params = parse_command()
                continue

            field = params[0]
            value = params[1]

            if field == "eq":
                market.trade_good_status[tg].equilibrium_quantity = value
                market.sell_order[tg].quantity = max(2 * market.trade_good_status[tg].equilibrium_quantity - market.trade_good_status[tg].total_supply, 0)
                print(f"Changed {tg}' Equilibrium amount to {value}")

            market.update_available_supply(tg)
            market.recalculate_prices(tg, "", False)

        if command == "help":
            display_help()

        if command is not None and command[-1] == "l":
            market.detailed_listing(tg, user.items)

        command, params = parse_command()

