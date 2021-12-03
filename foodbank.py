import math
import random


class FoodBank:
    def __init__(self, id, goal_factor, budget):
        self.id = id
        self.goal_factor = goal_factor
        self.budget = budget
        self.utility = 0
        self.perishable_value = None
        self.non_perishable_value = None


    def bid(self, num_items):
        return [random.uniform(0,1) for _ in range(num_items)]