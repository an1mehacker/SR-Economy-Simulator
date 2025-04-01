My attempt at creating a dynamic economy inspired by the game Space Rangers HD: A War Apart along with the changes that I think makes trading more interesting.

To use this project, run main.py and enter a desired amount for the market parameters

# Features
- One Market class is generated to display a trade good.
- Type commands to buy or sell goods and see the changes.
- Multiple corporations will spawn each with different qualities and price ranges
- A supply of trade goods will be distributed among the corporations
- An equilibrium quantity will determine the status of the trade good: Deficit, Balanced or Surplus
- The prices will reflect the status following supply and demand law 
- When supply is low, selling prices approach buying prices to incentivize selling
- Market allocates 75% of the equilibrium amount to its own internal supply that the player cannot interact with, to avoid a player induced deficit
- Bracketed Pricing - Prices recalculate after reaching critical breakpoints

Here's an example use
![](images/pic1.png?)


Most important file is economy_entity.py

Most important functions are: Market.generate_new_ees(), get_final_price_by_order, calculate_price_logistic, OrderListing.get_price

# Price factors

Global:
  * Inflation   
  * Trade Difficulty of Simulation
  * Trade Good Base Price and Range

Market:
  * Market Score (highly developed planets have more expensive goods)
  * Quality of Goods (from D to A)
  * Daily Fluctuation
  * Market Events like deficits or sales.
  * Supply and Demand

# Planned features
- More user interaction in the form of commands like auto-buying/selling from multiple EEs at once.
- Add an inventory where the user can track of their purchased items and money.
- Interact with multiple trade goods not just Technology Goods
- When Selling, your trade goods need to be of a certain quality.
- In addition to Enterprise Economy Entity (EE), add many smaller in quantity Individual EE
- Passage of time and price adjustment over time to reflect new supply
- Buying from one Market and selling it to another and see the changes in price
- Add interaction with Trade Good Legality and Essential status
- Add random events where prices change
- Add some kind of supply chains where to produce certain goods you need others
- Item grouping by price, place of origin and quality.
- Procedurally generate markets based on several factors like culture, political system and population

# Data Structures
### SimulationStatus:
Global information about the simulation that applies to all markets

### Market
A Market is a collection of corporations and individuals (Economy Entities) that are part of a single Planet or Space Station.
Within a market you will conduct trades
  - Collection of Order Listing grouped by trade good type
  - Collection of TradeGoodStatus grouped by trade good type

### TradeGoodStatus
Contains parameters and modifiers that apply to an entire market
  - Trade Good to modify, price range modifiers, essential, legality, equilibrium quantity

### Order Listing
Information about an individual demand to buy or sell an amount of goods
  - Operation (buy or sell), supply or demand quantity, price point modifier
  - The Economy Entity it belongs to

### Economy Entity
Buys and sells trade goods
An EE can produce more than one trade good. For example medicine and drugs. Or Common and Rare Minerals.
    - Name and Type

### Trade Good Item (Planned)
Whenever you buy trade goods, they're converted to items and placed on your inventory
  - Name
  - Price Bought
  - Place of origin
  - Legality (This is purely aesthetical)
  - Quantity
