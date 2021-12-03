import math
import random
import copy


class BNEFoodBank:
    def __init__(self, id, goal_factor=1, budget=100):
        self.id = id
        self.goal_factor = goal_factor
        self.budget = budget
        self.utility = 0
        self.values = []

    def bid(self,num_banks):
        '''
        # This is hardcoded for 2 items: [perishable, non-perishable]. If there are more items, this will need to be changed
        if self.values[0] + self.values[1] > self.budget:
            if self.values[0] > self.values[1]:
                # Can also bid the remaining budget on the other item
                return (max(self.values[0], self.budget), 0)
            else:
                return (0, max(self.values[1], self.budget))
        else:
            return (self.values[0], self.values[1])
        '''
        
        # This may work for more than 2 items
        bids = copy.deepcopy(self.values)
        bids = [bid * (num_banks - 1)/num_banks for bid in bids]
        # If total value exceeds budget, prioritize the highest value items. 
        while sum(bids) > self.budget:
            min_nonzero = float("inf")
            index = -1
            for i, val in enumerate(bids):
                if val > 0 and val < min_nonzero:
                    index = i
                    min_nonzero = val
            if sum(bids) - self.budget > min_nonzero:
                bids[index] = 0
            # Optional: This ensures that all budget is allocated. Can delete this if only want to bid on items where there is enough budget to
            # go along with the strategy (this will usually lead to one less item being bid on)
            else:
                bids[index] -= sum(bids) - self.budget
            
        return bids




            