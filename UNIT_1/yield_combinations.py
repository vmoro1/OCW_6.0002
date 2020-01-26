#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 12:31:05 2019

@author: viggomoro
"""

def powerSet(items):
    N = len(items)
    for i in range(2**N):
        combo = []
        for j in range(N):
            if (i >> j) % 2 == 1:
                combo.append(items[j])
        yield combo
    

def yieldAllCombos(items):
    """
    Generates all combinations of N items into two bags whereby each 
    item is in one or none of the bags.
    Yields a tuple, (bag1, bag2), where each bag is represented as a list 
    of which item(s) are in each bag.
    """
    N = len(items)
    for i in range(3**N):
        bag1 = []
        bag2 = []
        for j in range(N):
            if (i // (3**j)) % 3 == 1:
                bag1.append(items[j])
            if (i // (3**j)) % 3 == 2:
                bag2.append(items[j])
        yield (bag1, bag2)