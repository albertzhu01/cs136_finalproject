import itertools
import logging
import math
import random
import sys

from truthfulfoodbank import TruthfulFoodBank

from util import argmax_index

num_banks = 5
num_days = 100
num_items = 2

banks = [TruthfulFoodBank(id=id,goal_factor=1,budget=100) for id in range(num_banks)]

# list of goal factors for each bank
goal_factors = [bank.goal_factor for bank in banks]

# list of amount of food received by each bank
food_received = [0] * num_banks

for _ in range(num_days):
    print(f"-------------DAY {_}-------------")
    for b in banks:
        b.values = []
        # Perishable value
        b.values.append(random.uniform(20, 30))
        # Nonperishable value
        b.values.append(random.uniform(20, 50))

    # Allocate food items
    total_spent = 0
    for i in range(num_items):
        # The paper ranks banks by amount of food below the goal factor, so here I
        # just used the ratio of food received to goal factor to rank banks for each
        # item. Using difference of the two basically gives the same results so either
        # one should be fine in the end if we do this.
        ranking = [food - goal_f for food, goal_f in zip(food_received, goal_factors)]
        sorted_banks = [bank for _, bank in sorted(zip(ranking, banks), key=lambda pair: pair[0])]
        winner_id = banks.index(sorted_banks[0])
        winning_bank = banks[winner_id]
        food_received[winner_id] += 1

        # utility increases by either the perishable value or nonperishable value
        winning_bank.utility += winning_bank.values[i]
        print(f"Bank {winner_id} is allocated item {i}")

# Print utilities
print(f"-------------RESULTS-------------")
for b in banks:
    print(f"Bank {b.id} utility: {b.utility}")
    print(f"Bank {b.id} food: {food_received[b.id]}")
