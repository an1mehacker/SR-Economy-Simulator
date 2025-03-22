import random

from economy_entity import *
from enterprise_name_generator import trade_good_types
from normalrandom import trade_good_distribution, random_bell_curve

def clamp(value, lower, upper):
    return lower if value < lower else upper if value > upper else value

if __name__ == "__main__":
    simulation_status = SimulationStatus()
    """Singleton test
    simulation_status2 = SimulationStatus()
    simulation_status2.inflation = 2.0
    print(simulation_status.inflation)
    #"""

    trade_difficulty = clamp(int(input("Input a trade difficulty. Higher difficulty decreases the spread of prices (1 - 10) > ")), 1, 10)
    simulation_status.trade_difficulty = trade_difficulty
    calculate_price_ranges(trade_difficulty)

    # determine trade status, equilibrium quantity and current quantity
    equilibrium = int(input("Input an Equilibrium Supply > "))  # 500
    supply = int(input("Input a Current Supply > "))  # 480

    # market score determines development level, highly developed markets's goods are more expensive
    market_score = clamp(float(input("Input a Development score. Higher score makes prices higher (0.8x - 1.2x) > ")), 0.8, 1.2)
    market = Market.generate_market("Planet", equilibrium, supply, market_score, 0)

    player_input = input("w to wait, q to quit :> ")
    while player_input.lower() != "q" or player_input.lower() != "quit" or player_input.lower() != "exit":
        if player_input.lower() == "w" or player_input.lower() == "wait":
            print("\n" * 10)
            market.recalculate_prices()
            market.trade_good_listing("Technology Goods")
            print(market.trade_good_status["Technology Goods"].daily_fluctuation)

        player_input = input("w to wait, q to quit, b [quantity] to buy and s [quantity] to sell :> ")
    # market.summary_listing("Technology Goods")
