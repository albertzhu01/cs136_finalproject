import math
import random


class FoodBank:
    def __init__(self, id, goal_factor, perishable_value, non_perishable_value, budget):
        self.id = id
        self.goal_factor = goal_factor
        self.perishable_value = perishable_value
        self.non_perishable_value = non_perishable_value
        self.budget = budget
        self.utility = 0

    def bid(self, num_items):
        return [random.uniform(0,1) for _ in range(num_items)]