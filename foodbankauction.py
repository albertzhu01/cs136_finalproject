import itertools
import logging
import math
import random
import sys

from foodbank import FoodBank

from util import argmax_index

num_banks = 2
num_days = 10
num_items = 2

banks = [FoodBank(id,1,0) for id in range(num_banks)]


for _ in range(num_days):
    # Set value of the perishable and non-perishable food item(s)
    for bank in banks:
        bank.perishable_value = random.uniform(0,1)
        bank.non_perishable_value = random.uniform(0,1)

    # Collect bids
    bids = [bank.bid(num_items) for bank in banks]

    # Allocate food items
    total_spent = 0
    for i in range(num_items):
        winner_id = argmax_index([bid[i] for bid in bids])
        winning_bank = banks[winner_id]
        winning_bid = bids[winner_id][i]

        total_spent += winning_bid

        winning_bank.budget -= winning_bid

        # TODO
        winning_bank.utility += winning_bank.perishable_value
        
    # Redistribute currency
        total_goal_factor = sum([bank.goal_factor for bank in banks])
        for bank in banks:
            bank.budget += total_spent*(bank.goal_factor)/total_goal_factor

# Print utilities

print([(b.id, b.utility) for b in banks])
