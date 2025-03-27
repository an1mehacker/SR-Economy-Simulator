import re

from economy_entity import *
from math2 import clamp

def parse_command(user_input):
    processed_input = user_input.strip().lower()
    groups = processed_input.split()

    if not groups:
        return None, []

    operation = groups[0]
    params = groups[1:]

    params = [int(param) if param.isdigit() else param for param in params]

    if operation in {"q", "quit", "exit"}:
        return "q", []  # e.g., ('w', None) or ('quit', None)

    if operation in {"h", "help"}:
        return "h", params

    return operation, params  # Invalid input

if __name__ == "__main__":
    simulation_status = SimulationStatus()
    """Singleton test
    simulation_status2 = SimulationStatus()
    simulation_status2.inflation = 2.0
    print(simulation_status.inflation)
    #"""

    trade_difficulty = clamp(int(input("Input a trade difficulty. Higher difficulty tightens the spread of prices (1 - 10) > ")), 1, 10)
    simulation_status.trade_difficulty = trade_difficulty
    calculate_price_ranges(trade_difficulty)

    # determine trade status, equilibrium quantity and current quantity
    equilibrium = int(input("Input an Equilibrium Supply > "))  # 500
    supply = int(input("Input a Current Supply > "))  # 480
    tg = "Technology Goods"

    # market score determines development level, highly developed markets's goods are more expensive
    market_score = clamp(float(input("Input a Development score. Higher score makes prices higher (0.8x - 1.2x) > ")), 0.8, 1.2)
    market = Market.generate_market("Planet", equilibrium, supply, market_score)

    market.detailed_listing(tg)
    player_input = input("w to wait, q to quit, b [corporation index] [quantity]  to buy, s [corporation index] [quantity] to sell, h or help for command list :> ")
    command, params = parse_command(player_input)

    while command != "q" :

        if command == "b":
            if len(params) >= 2:
                quantity = int(params[1])
                if int(params[1]) > 0:
                    quantity = market.buy_sell(params[0] - 1, "Technology Goods", params[1], "Buy")
                    print(f"You bought {quantity} goods from corporation {params[0]}!")
                else:
                    print("Please input a positive integer number")

        if command == "s":
            if len(params) >= 2:
                quantity = market.buy_sell(params[0] - 1, "Technology Goods", params[1], "Sell")
                print(f"You sold {quantity} goods from corporation {params[0]}!")

        if command == "h":
            print("w to wait\nq to quit\nb [corporation index] [quantity] to buy\ns [corporation index] [quantity] to sell\nh or help for command list ")

        market.detailed_listing(tg)
        player_input = input("> ")
        command, params = parse_command(player_input)

