from market import *
from math2 import clamp

def parse_command(user_input):
    processed_input = user_input.strip().lower()
    groups = processed_input.split()

    if not groups:
        return None, []

    operation = groups[0]
    parameters = groups[1:]

    parameters = [int(param) if param.isdigit() else param for param in parameters]

    if operation in {"b", "buy"}:
        return "b", parameters

    if operation in {"s", "sell"}:
        return "s", parameters

    if operation in {"da", "dr", "bl", "sl", "w"}:
        return operation, parameters

    if operation in {"q", "quit", "exit"}:
        return "q", []  # e.g., ('w', None) or ('quit', None)

    if operation in {"h", "help"}:
        return "h", parameters

    if operation in {"l", "list"}:
        return "l", parameters

    return None, None  # Invalid input

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
            "Enter trade difficulty (1-10), equilibrium supply, current supply, and development score (0.8-1.2) separated by spaces\nOr press Enter for default values (1 500 500 1)\n> ")

        if setup_input.strip() == "":
            trade_difficulty, equilibrium, supply, development_score = 1, 500, 500, 1.0
            break

        try:
            trade_difficulty, equilibrium, supply, development_score = setup_input.split()

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
    #market.add_goods(tg, 5139)

    filtered_ees = market.detailed_listing(tg)
    command_input = input("w to skip time\nq to quit\nb [corporation index] [quantity] to buy\ns [corporation index] [quantity] to sell\nl to show detailed listing\nh or help for complete command list\n> ")
    command, params = parse_command(command_input)

    while command != "q" :

        if command is None:
            print("Invalid command. Type h for complete command list")

        if command == "b" or command == "bl":
            if len(params) >= 2:
                if 0 < int(params[0]) < len(market.buy_orders[tg]) + 1 and int(params[1] > 0):
                    quantities, prices, order = market.buy_sell(market.buy_orders[tg], params[0] - 1, "Technology Goods", params[1], "Buy")
                    if len(quantities) == 1 and quantities[0] > 0:
                        print(f"You bought {quantities[0]} {tg} from {order.economy_entity.name} for a total of {order.calculated_price * quantities[0]}cr!")
                    elif len(quantities) > 1:
                        yep = list(zip(quantities, prices))
                        cost = 0
                        for o in yep:
                            cost += o[0] * o[1]
                            print(f"You bought {o[0]} {tg} from {order.economy_entity.name} at {o[1]}cr each")

                        print(f"Totaling {sum(quantities)} {tg} for {cost}cr!")
                    else:
                        print("Need at least 1 unit to buy")
                else:
                    print("Input a valid corporation index number and a positive quantity number")
            else:
                print(f"Usage: b{"l" if command == "bl" else ""} [corporation index] [quantity]")

        if command == "s" or command == "sl":
            if len(params) >= 2:
                if 0 < int(params[0]) < len(market.buy_orders[tg]) + 1 and int(params[1] > 0):
                    quantities, prices, order = market.buy_sell(market.sell_orders[tg], params[0] - 1, "Technology Goods", params[1], "Sell")
                    if len(quantities) == 1:
                        print(f"You sold {quantities[0]} {tg} to {order.economy_entity.name} for a total of {order.calculated_price * quantities[0]}cr!")
                    else:
                        print("Need at least 1 unit to sell")
                else:
                    print("Input a valid corporation index number and a positive quantity number")
            else:
                print(f"Usage: s{"l" if command == "bl" else ""} [corporation index] [quantity]")

        if command == "da":
            if len(params) >= 2 and 0 < int(params[0]) < len(market.buy_orders[tg]) + 1 and int(params[1] > 0):
                added = market.add_goods(tg, params[0] - 1, params[1])
                print(f"Added {added} {tg} to the market!")

        if command == "dr":
            if len(params) >= 1 and int(params[0] > 0):
                removed = market.remove_goods(tg, params[0])
                print(f"Removed {removed} {tg} from the market!")

        if command == "h":
            print("w [number of days: optional] to skip time\n"
                  "q to quit\n"
                  "b [corporation index] [quantity] - to buy\n"
                  "s [corporation index] [quantity] - to sell\n"
                  "l - to show detailed listing. Can be appended to the first word of a command to execute both commands like bl or sl or abl \n"
                  "da [corporation index] [quantity] - to add goods to the market\n"
                  "dr [quantity] - to remove goods from the market\n"
                  "ab [quantity] [maximum price : optional] [minimum quality : optional] - Attempts to auto buy the selected quantity of goods starting by price ascending. Prioritizes higher quality goods when there's a price tie.\n"
                  "Can buy from multiple corporations. minimum quality default is 'C'. Will stop when quantity is reached or if there are no quantities available or if there are no goods with the minimum quality\n"
                  "as [quantity] [minimum price : optional] - Similar to auto buy, will attempt to auto sell all goods starting by price descending and prioritize lower quality goods to where it can be sold\n"
                  "h or help - show this command list ")

        if command in ["l", "bl", "sl"]:
            market.detailed_listing(tg)

        command_input = input("> ")
        command, params = parse_command(command_input)

