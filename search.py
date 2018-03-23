"""
File containing all the shit needed to search the state space
"""


class Graph:
    def __init__(self):
        pass


class Node:

    def __init__(self, state, parent=None, action=None, path_cost=None):
        """Creates a node in a search tree"""
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0

        if parent:
            self.depth = parent.depth + 1



    def child_node(self, problem, action):
        next_state = problem.result(self.state, action)

        return Node(next_state, self, action, self.path




