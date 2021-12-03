import itertools
import logging
import math
import random
import sys

from foodbank import FoodBank

from util import argmax_index

num_banks = 5
num_days = 100
num_items = 2

banks = [FoodBank(id=_,goal_factor=1,budget=100) for _ in range(num_banks)]



for _ in range(num_days):
    print(f"-------------DAY {_}-------------")
    for b in banks:
        print(f"Bank {b.id}'s budget is {b.budget}")

    # TODO: Currently hardcoded for 2 items.
    # Set value of the perishable and non-perishable food item(s).
    for b in banks:
        b.values = []
        # Perishable value
        b.values.append(random.uniform(20,30))
        # Nonperishable value
        b.values.append(random.uniform(20,50))

    # Collect bids
    bids = [b.bid() for b in banks]

    # Allocate food items
    total_spent = 0
    for i in range(num_items):
        winner_id = argmax_index([bid[i] for bid in bids])
        winning_bank = banks[winner_id]
        winning_bid = bids[winner_id][i]

        if winning_bid > 0:
            print(f"Bank {winner_id} wins item {i} with a bid of {winning_bid}")
            total_spent += winning_bid
            winning_bank.budget -= winning_bid
            winning_bank.utility += winning_bank.values[i]
        else:
            print(f"No banks bid on item {i}")
        
    # Redistribute currency
        total_goal_factor = sum([bank.goal_factor for bank in banks])
        for bank in banks:
            bank.budget += total_spent*(bank.goal_factor)/total_goal_factor

# Print utilities
for b in banks:
    print(f"Bank {b.id} utility: {b.utility}")
