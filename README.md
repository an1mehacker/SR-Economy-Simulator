My attempt at creating a dynamic economy inspired by the game Space Rangers HD: A War Apart along with changes that I think makes trading more interesting.

Summary:
- One Market class is generated to display a trade good.
- Multiple corporations will spawn each with different qualities and price ranges
- A supply of trade goods will be distributed among the corporations
- An equilibrium quantity will determine the status of the trade good: Deficit, Balanced or Surplus
- The prices will reflect the status following supply and demand law
- When supply is low, selling prices approach buying prices to incentivize selling

Most important file is economy_entity.py

Most important functions are: Market.generate_new_ees(), get_final_price_by_order, calculate_price_logistic, OrderListing.get_price

Changes to SR:
* In addition to legality of trade goods, they also have whether or not they're essential. Food and Medicine goods are essential for example and are more resistant to price changes across one Market.
* Trade Goods have a Quality indicator. Higher quality goods are generally more expensive. When Selling, your trade goods need to be of a certain quality.
* Trade goods can be purchased from different corporations and individuals with a small price spread between them.
* More trade goods
* Grouping same trade goods by price, place of origin and quality.

Buying and selling price are determined by many factors such as: Inflation (Global), Market Score (highly developed planets have more expensive goods), Quality of Goods (from D to A), Daily Fluctuation and Market Events like deficits or sales.

TODO:
- Add user interaction in the form of commands
- Passsage of time
- Buying from one Market and selling it to another and see the changes in price
- Bracketed Pricing - The price of goods changes after a certain quantity reaches a critical deficit or surplus point. Example: buying 100 units costs 20cr each. But buy 101 units and the 101st unit costs 25cr as well as every new unit beyond. Similar how it works in Starsector or X4.
- Add some kind of supply chains where to produce certain goods you need others
- Add random events where prices change
- Add price adjustment over time to reflect new supply

Market:
  A Market is a collection of corporations and individuals (Economy Entities) that are part of a single Planet or Space Station.
  - Collection of Economy Entities
  - Collection of TradeGoodStatus

TradeGoodStatus:
  - Trade Good to modifiy, price range modifiers, essential, legality, equilibrium quantity

Economy Entity:
An EE can produce more than one trade good. For example medicine and drugs. Or Common and Rare Minerals.
  - Collection of Order Listing

Order Listing:
  - Operation (buy or sell), supply or demand quantity, price point modifier

Trade Good (Item):
  - Name
  - Price Bought
  - Place of origin
  - Legality (This is purely aesthetical)
  - Quantity
