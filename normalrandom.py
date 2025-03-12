import random

def random_bell_curve(min, max):
  distanceFromMedian = random.uniform(0, (max - min) / 2.0)

  return min + ((max - min) / 2.0 + distanceFromMedian * (-1) ** (random.randrange(-1, 0)))


def trade_good_distribution2(total_goods, num_slots, spread_multiplier=0.75):
    """
    Distributes total_goods into num_slots using a smooth descending pattern with controlled randomness.

    :param total_goods: int - Total amount of goods to distribute.
    :param num_slots: int - Number of slots/entities to distribute among.
    :param spread_multiplier: smaller values like 0.5 produce a more balanced distribution
    :return: List[int] - Distributed values in descending order.
    """
    # Modify the magic value for a different spread smoothness
    base_pattern = [num_slots - (i * spread_multiplier) for i in range(num_slots)]
    pattern_sum = sum(base_pattern)

    # Scale pattern values proportionally to match total_goods
    distribution = [(x / pattern_sum) * total_goods for x in base_pattern]

    # Apply controlled randomness
    random_variation = [random.randint(i, 50+i) - random.randint(0, 3*i) for i in range(num_slots)]

    # Adjust the first half positively, last half negatively
    for i in range(num_slots):
        if i < num_slots // 2:  # First half gets more positive variation
            distribution[i] += abs(random_variation[i])
        else:  # Last half gets slight reductions
            distribution[i] -= abs(random_variation[i]) * 0.25

    # Convert to integers and fix rounding errors
    distribution = [max(0, int(x)) for x in distribution]  # Prevent negatives
    difference = total_goods - sum(distribution)

    # Balance rounding errors by adjusting first few slots
    for i in range(abs(difference)):
        distribution[i % num_slots] += 1 if difference > 0 else -1

    #print(distribution)
    #print(sum(distribution))
    return distribution

def trade_good_distribution(total_goods, num_slots, spread_multiplier=0.75):
    """
    Distributes total_goods into num_slots using a smooth descending pattern with controlled randomness.

    :param total_goods: int - Total amount of goods to distribute.
    :param num_slots: int - Number of slots/entities to distribute among.
    :param spread_multiplier: float - Controls spread smoothness (0.5 for balanced, 1.0 for steep drop-off).
    :return: List[int] - Distributed values in descending order.
    """
    if total_goods <= 0 or num_slots <= 0:
        return [0] * num_slots  # Edge case: No goods to distribute

    # Generate a smooth descending base pattern
    base_pattern = [max(0.1, num_slots - (i * spread_multiplier)) for i in range(num_slots)]
    pattern_sum = sum(base_pattern)

    # Scale pattern to match total_goods
    distribution = [(x / pattern_sum) * total_goods for x in base_pattern]

    # Apply controlled randomness based on available supply
    max_variation = max(1, total_goods // num_slots)  # Ensure reasonable variation
    random_variation = [random.randint(-max_variation, max_variation) for _ in range(num_slots)]

    # Adjust values while preventing negatives
    for i in range(num_slots):
        if i < num_slots // 2:  # Early values get slight positive variation
            distribution[i] += abs(random_variation[i])
        else:  # Later values get slight reductions
            distribution[i] -= abs(random_variation[i]) * 0.25

    # Convert to integers and prevent negatives
    distribution = [max(0, round(x)) for x in distribution]

    # Ensure total sums up correctly
    difference = total_goods - sum(distribution)
    for i in range(abs(difference)):
        if difference > 0:
            distribution[i % num_slots] += 1  # Add to the first elements
        elif difference < 0 and distribution[i % num_slots] > 0:
            distribution[i % num_slots] -= 1  # Remove from nonzero elements

    return distribution


[random.randint(i, 10+i) - random.randint(0, i) for i in range(7)]

def trade_good_distribution2(initial_trade_goods, max_amount_of_distributions):
    trade_goods = initial_trade_goods
    ees = []
    temp = 0

    for i  in range(0, max_amount_of_distributions):
        #n = random.triangular(0, 1)
        n = random_bell_curve(0, 1)
        #print(n)
        current_ee = round(n * trade_goods) + 1

        if current_ee + temp < initial_trade_goods * 0.01:
            temp = temp + current_ee
            continue
        """
        if current_ee == 0:
            current_ee = current_ee + trade_goods
            ees.append(current_ee)
            break"""

        trade_goods = trade_goods - current_ee - temp
        ees.append(current_ee + temp)
        temp = 0

    ees.sort(reverse=True)
    print(ees)

#trade_good_distribution(1000, 10)
'''
for i in range(0, 1000):
    for i  in range(0, 5):
        #n = random.triangular(0, 1)
        n = randombellcurve(0, 1)
        print(n)
        current_ee = round(n * tradegoods)
        if (current_ee == 0):
            continue

        tradegoods = tradegoods - current_ee
        ees.append(current_ee)
    tradegoods = 1000
    ees.sort(reverse=True)
    topvalues.append(ees[0])
    ees.clear()

topvalues.sort(reverse=True)
print(topvalues)

'''