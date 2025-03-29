import re

from market import *
from math2 import clamp

def parse_command(user_input):
    processed_input = user_input.strip().lower()
    groups = processed_input.split()

    if not groups:
        return None, []

    operation = groups[0]
    params = groups[1:]

    params = [int(param) if param.isdigit() else param for param in params]

    if operation in {"b", "buy"}:
        return "b", params

    if operation in {"s", "sell"}:
        return "s", params


    if operation in {"bl"}:
        return "bl", params

    if operation in {"sl"}:
        return "sl", params

    if operation in {"w"}:
        return "w", params

    if operation in {"q", "quit", "exit"}:
        return "q", []  # e.g., ('w', None) or ('quit', None)

    if operation in {"h", "help"}:
        return "h", params

    if operation in {"l", "list"}:
        return "l", params

    return None, None  # Invalid input

if __name__ == "__main__":
    simulation_status = SimulationStatus()
    """Singleton test
    simulation_status2 = SimulationStatus()
    simulation_status2.inflation = 2.0
    print(simulation_status.inflation)
    #"""

    while True:
        user_input = input(
            "Enter trade difficulty (1-10), equilibrium supply, current supply, and development score (0.8-1.2) separated by spaces\nOr press Enter for default values (1 500 500 1)\n> ")

        if user_input.strip() == "":
            trade_difficulty, equilibrium, supply, development_score = 1, 500, 500, 1.0
            break

        try:
            trade_difficulty, equilibrium, supply, development_score = user_input.split()

            trade_difficulty = clamp(int(trade_difficulty), 1, 10)
            equilibrium = int(equilibrium)
            supply = int(supply)
            development_score = clamp(float(development_score), 0.8, 1.2)
            break
        except ValueError:
            print("Invalid input, enter something like '2 500 300 0.9'")


    simulation_status.trade_difficulty = trade_difficulty
    calculate_price_ranges(trade_difficulty)

    tg = "Technology Goods"
    market = Market.generate_market("Planet", equilibrium, supply, development_score)

    filtered_ees = market.detailed_listing(tg)
    player_input = input("w to skip time\nq to quit\nb [corporation index] [quantity] to buy\ns [corporation index] [quantity] to sell\nl to show detailed listing\nh or help for complete command list\n> ")
    command, params = parse_command(player_input)

    while command != "q" :

        if command is None:
            print("Invalid command. Type h for complete command list")

        if command == "b" or command == "bl":
            if len(params) >= 2:
                quantity = int(params[1])
                if 0 < int(params[0]) < len(market.buy_orders[tg]) + 1 and int(params[1] > 0):
                    quantity, order = market.buy_sell(market.buy_orders[tg], params[0] - 1, "Technology Goods", params[1], "Buy")
                    if quantity > 0:
                        print(f"You bought {quantity} {tg} from {order.economy_entity.name} for a total of {order.calculated_price * quantity}cr!")
                    else:
                        print("Need at least 1 unit to buy")
                else:
                    print("Input a valid corporation index number and a positive quantity number")
            else:
                print(f"Usage: b{"l" if command == "bl" else ""} [corporation index] [quantity]")

        if command == "s" or command == "sl":
            if len(params) >= 2:
                if 0 < int(params[0]) < len(market.buy_orders[tg]) + 1 and int(params[1] > 0):
                    quantity, order = market.buy_sell(market.buy_orders[tg], params[0] - 1, "Technology Goods", params[1], "Sell")
                    if quantity > 0:
                        print(f"You sold {quantity} {tg} to {order.economy_entity.name} for a total of {order.calculated_price * quantity}cr!")
                    else:
                        print("Need at least 1 unit to sell")
                else:
                    print("Input a valid corporation index number and a positive quantity number")
            else:
                print(f"Usage: s{"l" if command == "bl" else ""} [corporation index] [quantity]")

        if command == "h":
            print("w [number of days: optional] to skip time\n"
                  "q to quit\n"
                  "b [corporation index] [quantity] - to buy\n"
                  "s [corporation index] [quantity] - to sell\n"
                  "l - to show detailed listing. Can be appended to the first word of a command to execute both commands like bl or sl or abl \n"
                  "ab [quantity] [maximum price : optional] [minimum quality : optional] - Attempts to auto buy the selected quantity of goods starting by price ascending. Prioritizes higher quality goods when there's a price tie.\n"
                  "Can buy from multiple corporations. minimum quality default is 'C'. Will stop when quantity is reached or if there are no quantities available or if there are no goods with the minimum quality\n"
                  "as [quantity] [minimum price : optional] - Similar to auto buy, will attempt to auto sell all goods starting by price descending and prioritize lower quality goods to where it can be sold\n"
                  "h or help - show this command list ")

        if command[-1] == 'l':
            market.detailed_listing(tg)

        player_input = input("> ")
        command, params = parse_command(player_input)

