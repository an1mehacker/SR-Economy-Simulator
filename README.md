My attempt at creating a dynamic economy inspired by the game Space Rangers HD: A War Apart along with the changes that I think makes trading more interesting.

To use this project, run main.py and enter a desired amount for the market parameters

# Features
- Buy from multiple Producers at different prices and sell them with your bought items
- Prices reflect Supply and Demand Law determined by the Market's Equilibrium and Current Supply quantities.
- Selling prices approach buying prices to incentivize selling when supply is low
- Internal Supply - 75% of the equilibrium amount is reserved only for the market, to avoid a player induced deficit
- Passage of Time - Prices rise and fall over time towards a new price when supply is affected, fluctuate over time and grow to reflect a rising inflation
- Delayed Self-balancing market - over time buying will add equal demand to selling and vice versa when at a surplus
- Bracketed Pricing - Prices recalculate after reaching critical breakpoints to avoid being rewarded for flooding a market

Here's an example use
![](images/pic1.png?)

Most important file is economy_entity.py

Most important functions are: Market.generate_new_ees(), Market.buy(), Market.sell(), calculate_price_point(), 

# Price factors

Global:
  * Inflation   
  * Trade Difficulty of Simulation
  * Trade Good Base Price and Range

Market:
  * Development Score (highly developed planets have more expensive goods)
  * Producer Bonuses if applicable
  * Daily Fluctuation
  * Market Events like deficits or sales.
  * Supply and Demand

# Planned features
- Change breakpoints for every 25% of equilibrium from 0 to 200% instead of at fixed values
- Generate all trade goods
- In addition to Enterprise Producers, add many smaller in quantity Individual Producers
- Buying from one Market and selling it to another and see the changes in price
- Add interaction with Trade Good Legality and Essential status
- Producer Bonuses. Check bonuses on other markets and seek the corresponding producers that get rewarded for more profit
- Add some kind of supply chains where to produce certain goods you need others
- Procedurally generate markets based on several factors like culture, political system and population
- Profit indicator when selling that displays profit margins 
- Price restrictions based on market's conditions
- Unit testing to make sure all these complex calculations and interactions are actually behaving as intended
- Client side only implementation on a website

# Data Structures
### SimulationStatus:
Global information about the simulation that applies to all markets

### Market
A Market is a collection of OrderListings that are part of a single Planet or Space Station.
  - Collection of Order Listing and a single Sell Listing grouped by trade good type
  - Collection of TradeGoodStatus grouped by trade good type
  - Development Score that affects all prices on the market

### TradeGoodStatus
Keeps track of vital information about a trade good of a market
  - Daily Fluctuation
  - Producer Modifiers
  - Whether the trade good is essential and legal
  - Equilibrium and Supply quantity
  - Current Market Situation - Balanced, Deficit, Surplus
  - Generic Price Points

### Order Listing and Sell Listing
Information about a demand to buy or sell an amount of goods
  - Supply or demand quantity
  - Price point modifier that gets calculated based on Supply Ratio, Development Score and Producer Variation if applicable
  - The Producer that the order belongs to if applicable

### Producer
Produces goods and lists them on the market.

A Producer can produce more than one trade good. For example medicine and drugs. Or Common and Rare Minerals.
  - Name 
  - Type : Enterprise or Individual
  - Variation Modifier - Modifier that applies to all of its orders' prices

### Trade Good Item
Whenever you buy trade goods, they're converted to items and placed on your inventory where you can then sell them
  - Name
  - Price Bought
  - Place of origin
  - Producer
  - Legality (This is purely aesthetical for now)
  - Quantity

### Actor
Someone who interacts with the market
  - Money
  - List of Items