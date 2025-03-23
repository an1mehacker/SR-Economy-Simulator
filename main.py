import re

from economy_entity import *
from math2 import clamp

def parse_command(user_input):
    user_input.strip().lower()
    match = re.fullmatch(r"([bs]) (\d+)", user_input)
    if match:
        command, quantity = match.groups()
        return command, int(quantity)  # Returns ('b', 100) or ('s', 50)

    # Handle single-word commands (w, q, quit, exit)

    if user_input in {"w"}:
        return user_input, None  # e.g., ('w', None) or ('quit', None)

    if user_input in {"q", "quit", "exit"}:
        return "q", None  # e.g., ('w', None) or ('quit', None)

    return None, None  # Invalid input

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

    # market score determines development level, highly developed markets's goods are more expensive
    market_score = clamp(float(input("Input a Development score. Higher score makes prices higher (0.8x - 1.2x) > ")), 0.8, 1.2)
    market = Market.generate_market("Planet", equilibrium, supply, market_score)

    player_input = input("w to wait, q to quit, b [quantity] [corporation index] to buy and s [quantity] [corporation index] to sell :> ")
    command, param1 = parse_command(player_input)
    while command != "q" :
        if command == "b":
            print(f"You bought {param1} goods!")

        if command == "s":
            print(f"You sold {param1} goods!")

        player_input = input("w to wait, q to quit, b [quantity] [corporation index] to buy and s [quantity] [corporation index] to sell :> ")
        command, param1 = parse_command(player_input)

