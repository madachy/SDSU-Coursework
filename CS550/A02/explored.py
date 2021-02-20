"""
Created on Feb 12, 2018

@author: Tom Paulus
@author: William Fox
"""


class Explored(object):
    """"Maintain an explored set.  Assumes that states are hashable"""

    def __init__(self):
        """"__init__() - Create an empty explored set"""

        self.hash_map = dict()

    def exists(self, state):
        """exists(state) - Has this state already been explored?
        Returns True or False, state must be hashable
        """

        try:
            return state in self.hash_map[hash(state)]
        except KeyError:
            return False

    def add(self, state):
        """add(state) - add given state to the explored set.  
        state must be hashable and we asssume that it is not already in set
        """

        # The hash function is a Python builtin that generates
        # a hash value from its argument.  Use this to create
        # a dictionary key.  Handle collisions by storing 
        # states that hash to the same key in a bucket list.
        # Note that when you access a Python dictionary by a
        # non existant key, it throws a KeyError

        if hash(state) not in self.hash_map.keys():
            self.hash_map[hash(state)] = set()
        self.hash_map[hash(state)].add(state)

