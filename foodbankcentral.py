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

banks = [FoodBank(id, 1, 0, 0, 0) for id in range(num_banks)]

for _ in range(num_days):
    # Allocate food items
    total_spent = 0
    for i in range(num_items):
        # need to somehow update the goal factor / figure out how to distribute
        # based on goal factor since rn the bank w highest goal factor just wins
        # everything
        winner_id = argmax_index([bank.goal_factor for bank in banks])
        winning_bank = banks[winner_id]

        # TODO
        # utility increases by either the perishable value or nonperishable value
        winning_bank.utility += winning_bank.perishable_value

# Print utilities
print([(b.id, b.utility) for b in banks])
