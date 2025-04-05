from market import *
from math2 import clamp

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
            "Enter trade difficulty (1-10), equilibrium supply, current supply, and development score (0.9-1.1) separated by spaces\nOr press Enter for default values (1 500 750 1)\n> ")
        setup_input2 = setup_input.strip().split()
        if not setup_input2:
            trade_difficulty, equilibrium, supply, development_score = 1, 500, 750, 1.0
            break

        try:
            trade_difficulty, equilibrium, supply, development_score = setup_input2

            trade_difficulty = clamp(int(trade_difficulty), 1, 10)
            equilibrium = int(equilibrium)
            supply = int(supply)
            development_score = clamp(float(development_score), 0.9, 1.1)
            break
        except ValueError:
            print("Invalid input, enter something like '2 500 300 0.9' or press Enter for default values (1 500 500 1)")

    simulation_status.trade_difficulty = trade_difficulty
    SimulationStatus().calculate_price_ranges(trade_difficulty)

    tg = "Technology Goods"
    market = Market.generate_market("Planet", equilibrium, supply, development_score)
    market.summary_listing(tg)
    print("\nType help for complete list of commands\n")
    command, params = parse_command()

    while command != "q" :

        if command is None:
            print("Invalid command. Type h for complete command list")

        if command in ["b", "bl", "s", "sl"]:
            operation = "Buy" if command in ["b", "bl"] else "Sell"
            if len(params) < 2:
                print(f"Usage: {"b" if operation == "Buy" else "s"}{'l' if command in ["bl", "sl"] else ''} [corporation index] [quantity]")
                command, params = parse_command()
                continue

            corp_index, quantity = int(params[0]), int(params[1])

            if not (0 < corp_index < len(market.buy_orders[tg]) + 1 and quantity > 0):
                print(f"Input a valid corporation index number 1 - {len(market.buy_orders[tg])} and a positive quantity number")
                command, params = parse_command()
                continue

            quantities, prices, order = market.buy_sell(market.buy_orders[tg] if operation == "Buy" else market.sell_orders[tg], corp_index - 1, tg, quantity, operation)

            if not quantities:
                print(f"Cannot {operation.lower()} on an order with 0 quantity")
                command, params = parse_command()
                continue

            if len(quantities) == 1:
                print(f"You {"bought" if operation == "Buy" else "sold"} {quantities[0]} {tg} {"from" if operation == "Buy" else "to"} {order.producer.name} for a total of {order.calculated_price * quantities[0]}cr!")
                command, params = parse_command()
                continue

            brackets = list(zip(quantities, prices))
            total_cost = sum(q * p for q, p in brackets)

            for q, p in brackets:
                print(f"You {"bought" if operation == "Buy" else "sold"} {q} {tg} at {p}cr each")

            print(f"Totaling {sum(quantities)} {tg} {"from" if operation == "Buy" else "to"} {order.producer.name} for {total_cost}cr!")

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
            market.detailed_listing(tg)

        command, params = parse_command()

