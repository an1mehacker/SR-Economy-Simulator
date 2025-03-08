Most important file is economy_entity.py
Most important functions are: Market.generate_new_ees(), get_final_price_by_order, calculate_price_logistic, OrderListing.get_price

Changes to SR:
* Trade Goods have a Quality indicator. Quality goods are generally more expensive.
* When Selling, your trade goods need to be of a certain quality.
* Trade goods can be purchased from different corporations and individuals with a small price spread between them.

A Market is a collection of corporations and individuals (Economy Entities) that are part of a single Planet or Space Station.

Buying and selling price are determined by many factors such as: Inflation (Global), Market Score (highly developed planets have more expensive goods), Quality of Goods (from D to A), Daily Fluctuation and Market Events like deficits or sales.

