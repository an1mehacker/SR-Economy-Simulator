import unittest
from config import *

class TestMarketSimulator(unittest.TestCase):

    def test_available_supply_matches_buy_orders(self):
        # Assume `get_all_markets()` is a function that returns your list of markets
        #markets = get_all_markets()  # Replace this with actual loading logic
        """
            for m in markets:
                for trade_good in TRADE_GOODS_DATA:
                    available = m.trade_good_status[trade_good].available_supply
                    counted = sum([o.quantity for o in m.buy_orders[trade_good]])
                    if available > 0 and available != counted:
                        print(f"Incorrect counting -> {m.name} - {trade_good}")
        """

        markets = []

        for market in markets:
            for trade_good in TRADE_GOODS_DATA:
                with self.subTest(market=market.name, trade_good=trade_good):
                    available = market.trade_good_status[trade_good].available_supply
                    counted = sum(order.quantity for order in market.buy_orders[trade_good])
                    self.assertEqual(
                        available,
                        counted,
                        f"Mismatch in {market.name} - {trade_good}: expected {available}, got {counted}"
                    )

if __name__ == "__main__":
    unittest.main()