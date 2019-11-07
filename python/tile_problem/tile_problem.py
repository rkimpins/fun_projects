# searchProblem.py - representations of search problems
# AIFCA Python3 code Version 0.7.6 Documentation at http://aipython.org

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en
from searchProblem import Search_problem, Arc
import random
import copy

class Tile_problem(Search_problem):

    def __init__(self, dim, start_state):
        self.dim = dim
        self.start_state = start_state

    def start_node(self):
        return self.start_state

    def is_goal(self, node):
        for item in node:
            if item == 1:
                return False
        return True

    def flip_tile(self, x, y, node):
        if x >= 0 and y >= 0 and x < self.dim and y < self.dim:
            temp = node[x + self.dim*y]
            if temp == 1:
                temp = node[x + self.dim*y] = 0
            else:
                temp = node[x + self.dim*y] = 1

    def flip_tile_set(self, x, y, node):
        self.flip_tile(x, y, node)
        self.flip_tile(x+1, y, node)
        self.flip_tile(x-1, y, node)
        self.flip_tile(x, y+1, node)
        self.flip_tile(x, y-1, node)

    def neighbors(self, node):
        neighbours = list()
        arcs = list()
        cost = 1
        for i in range(self.dim):
            for j in range(self.dim):
                new_node = copy.deepcopy(node)
                self.flip_tile_set(i, j, new_node)
                arcs.append(Arc(node, new_node, cost))
        return arcs
    def heuristic(self, n):
        total = 0
        for item in n:
            total += item
        return total
