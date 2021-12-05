import itertools
import logging
import math
import random
import sys
import numpy as np

from truthfulfoodbank import TruthfulFoodBank

from util import argmax_index

num_banks = 5
num_days = 100
num_items = 2
num_trials = 10

utilities_all_trials = []
food_offered_all_trials = []
food_received_all_trials = []

banks = [TruthfulFoodBank(id=_,goal_factor=random.uniform(0.5,1.5),budget=100) for _ in range(num_banks)]

for t in range(num_trials):

    # Reset banks' budgets and utilities
    for b in banks:
        b.budget = 100
        b.utility = 0

    # list of goal factors for each bank
    goal_factors = [bank.goal_factor for bank in banks]

    # list of amount of food received by each bank
    food_offered = [0] * num_banks
    food_received = [0] * num_banks

    for _ in range(num_days):
        print(f"-------------DAY {_}-------------")
        for b in banks:
            b.values = []
            # Perishable value
            b.values.append(random.normalvariate(25, 3))
            # Nonperishable value
            b.values.append(random.normalvariate(35, 9))

        # Allocate food items
        total_spent = 0
        for i in range(num_items):
            # The paper ranks banks by amount of food below the goal factor, so here I
            # just used the ratio of food received to goal factor to rank banks for each
            # item. Using difference of the two basically gives the same results so either
            # one should be fine in the end if we do this.
            ranking = [food/goal_f for food, goal_f in zip(food_offered, goal_factors)]
            sorted_banks = [bank for _, bank in sorted(zip(ranking, banks), key=lambda pair: pair[0])]
            winner_id = banks.index(sorted_banks[0])
            winning_bank = banks[winner_id]
            food_offered[winner_id] += 1
        
            # Bank only accepts the food if its value is high enough. If the bank rejects the food, 
            # the mechanism treats it as if the bank had accepted the food
            if winning_bank.values[i] > 22:
                food_received[winner_id] += 1
                winning_bank.utility += winning_bank.values[i]
                print(f"Bank {winner_id} receives item {i}")
            else:
                print(f"Bank {winner_id} was offered item {i} but rejected")

    # Add utilities, food received to running list
    utilities_all_trials.append([b.utility for b in banks])
    food_offered_all_trials.append(food_offered)
    food_received_all_trials.append(food_received)    

# Print results
print(f"-------------RESULTS-------------")
print(f"Number of trials: {num_trials}")

for b in banks:
    print(f"Bakn {b.id}'s goal factor: {b.goal_factor}")
    print(f"Bank {b.id}'s utility: {np.mean([u[b.id] for u in utilities_all_trials])} ({np.std([u[b.id] for u in utilities_all_trials])}) ")
    print(f"Bank {b.id}'s food offered : {np.mean([f[b.id] for f in food_offered_all_trials])} ({np.std([f[b.id] for f in food_offered_all_trials])})")
    print(f"Bank {b.id}'s food received : {np.mean([f[b.id] for f in food_received_all_trials])} ({np.std([f[b.id] for f in food_received_all_trials])})")

print(f"Average total food allocated: {np.sum(food_received_all_trials)}")
print(f"Average total food offered: {np.sum(food_offered_all_trials)}")
