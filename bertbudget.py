#!/usr/bin/env python

import sys

from gsp import GSP
from util import argmax_index

class Bertbudget:
    """Budget bidding agent"""
    def __init__(self, id, value, budget):
        self.id = id
        self.value = value
        self.budget = budget

    def initial_bid(self, reserve):
        return self.value / 2


    def slot_info(self, t, history, reserve):
        """Compute the following for each slot, assuming that everyone else
        keeps their bids constant from the previous rounds.

        Returns list of tuples [(slot_id, min_bid, max_bid)], where
        min_bid is the bid needed to tie the other-agent bid for that slot
        in the last round.  If slot_id = 0, max_bid is 2* min_bid.
        Otherwise, it's the next highest min_bid (so bidding between min_bid
        and max_bid would result in ending up in that slot)
        """
        prev_round = history.round(t-1)
        other_bids = [a_id_b for a_id_b in prev_round.bids if a_id_b[0] != self.id]

        clicks = prev_round.clicks
        def compute(s):
            (min, max) = GSP.bid_range_for_slot(s, clicks, reserve, other_bids)
            if max == None:
                max = 2 * min
            return (s, min, max)
            
        info = list(map(compute, list(range(len(clicks)))))
#        sys.stdout.write("slot info: %s\n" % info)
        return info


    def expected_utils(self, t, history, reserve):
        """
        Figure out the expected utility of bidding such that we win each
        slot, assuming that everyone else keeps their bids constant from
        the previous round.

        returns a list of utilities per slot.
        """
        prev_round = history.round(t - 1)
        clicks = prev_round.clicks
        info = self.slot_info(t, history, reserve)
        utilities = []

        for j in range(len(clicks)):
            payment = reserve if j >= len(info) else info[j][1]
            utilities.append(clicks[j] * (self.value - payment))

        return utilities

    def target_slot(self, t, history, reserve):
        """Figure out the best slot to target, assuming that everyone else
        keeps their bids constant from the previous rounds.

        Returns (slot_id, min_bid, max_bid), where min_bid is the bid needed to tie
        the other-agent bid for that slot in the last round.  If slot_id = 0,
        max_bid is min_bid * 2
        """
        i = argmax_index(self.expected_utils(t, history, reserve))
        info = self.slot_info(t, history, reserve)
        return info[i]

    def bid(self, t, history, reserve):
        # Get clicks from previous round, slot info, and utilities
        prev_round = history.round(t - 1)
        clicks = prev_round.clicks
        (slot, min_bid, max_bid) = self.target_slot(t, history, reserve)
        utilities = self.expected_utils(t, history, reserve)

        if utilities[slot] <= 0:
            return self.value
        else:
            # If it is the last round, bid the entire rest of the the budget
            if t == 47:
                return self.budget
            if slot > 0:
                bid = self.value - utilities[slot] / clicks[slot - 1]

                # If the prices are too high, reduce the bid to ensure that we don't
                # run out of budget
                if min_bid > self.budget / (48 - t):
                    bid *= ((self.budget / (48 - t)) / min_bid)
                return bid
            else:
                return self.value

    def __repr__(self):
        return "%s(id=%d, value=%d)" % (
            self.__class__.__name__, self.id, self.value)


