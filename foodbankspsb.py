import itertools
import logging
import math
import random
import sys
import numpy as np

from truthfulfoodbank import TruthfulFoodBank
from bnefoodbank import BNEFoodBank

from util import argmax_index

num_banks = 5
num_days = 100
num_items = 2
num_trials = 10

utilities_all_trials = []
food_received_all_trials = []

banks = [TruthfulFoodBank(id=_,goal_factor=random.uniform(0.5,1.5),budget=100) for _ in range(num_banks)]

for t in range(num_trials):

    # Reset banks' budgets and utilities
    for b in banks:
        b.budget = 100
        b.utility = 0

    # list of goal factors for each bank in case it's convenient to access as a list
    goal_factors = [bank.goal_factor for bank in banks]

    # list of amount of food received by each bank
    food_received = [0] * num_banks

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
        bids = [b.bid(len(banks)) for b in banks]

        # Allocate food items
        total_spent = 0
        for i in range(num_items):
            bids_i = [bid[i] for bid in bids]
            bids_i.sort()
            # print(bids_i)
            winner_id = argmax_index([bid[i] for bid in bids])
            winning_bid = bids_i[-1]
            # print(winner_id)
            # print(winning_bid)
            winning_bank = banks[winner_id]
            second_bid = bids_i[-2]

            if winning_bid > 0:
                print(f"Bank {winner_id} wins item {i} with a bid of {winning_bid} and payment {second_bid}")
                total_spent += second_bid
                winning_bank.budget -= second_bid
                winning_bank.utility += winning_bank.values[i]
                food_received[winner_id] += 1
            else:
                print(f"No banks bid on item {i}")
            
        # Redistribute currency
            total_goal_factor = sum([bank.goal_factor for bank in banks])
            for bank in banks:
                bank.budget += total_spent*(bank.goal_factor)/total_goal_factor

    # Add utilities, food received to running list
    utilities_all_trials.append([b.utility for b in banks])
    food_received_all_trials.append(food_received)

# Print results
print(f"-------------RESULTS-------------")
print(f"Number of trials: {num_trials}")

for b in banks:
    print(f"Bakn {b.id}'s goal factor: {b.goal_factor}")
    print(f"Bank {b.id}'s utility: {np.mean([u[b.id] for u in utilities_all_trials])} ({np.std([u[b.id] for u in utilities_all_trials])}) ")
    print(f"Bank {b.id}'s food received : {np.mean([f[b.id] for f in food_received_all_trials])} ({np.std([f[b.id] for f in food_received_all_trials])})")

