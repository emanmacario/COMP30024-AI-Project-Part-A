"""
File containing all the shit needed to search the state space
"""

import sys


class Graph:
    def __init__(self):
        pass


class Problem(object):
    """Absract class for a problem"""

    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state,
        and possibly a goal state, if there is a unique goal.
        """
        self.initial = initial
        self.goal = goal


    def actions(self, state):
        """Return the actions that can be executed in the given state"""
        pass


    def result(self, state, action):
        """Return the state that results from executing the given action
        in the state. The action must be one of self.actions(state)"""
        pass


    def goal_test(self, state):
        """Return True if the state is a goal"""
        pass


    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2
        from state1 via action, assuming cost c to get to state1.
        Default cost is 1 for every step"""
        return c + 1




class Node:

    """A node in a search tree"""

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
        """Create a new child node from this node, by applying
        a certain action to the current state"""
        next_state = problem.result(self.state, action)

        return Node(next_state, self, action, self.path)






def depth_limited_search(problem, limit=100):

    def recursive_dls(node, problem, limit):
        if problem.goal_test(node.state):
            return node
        elif limit == 0:
            return 'cutoff'
        else:
            cutoff_occurred = False
            for child in node.expand(problem):
                result = recursive_dls(child, problem, limit-1)
                if result == 'cutoff'
                    cutoff_occurred = True
                elif result is not None:
                    return result
            return 'cutoff' if cutoff_occurred else None


    # Body of depth-limited search
    return recursive_dls(Node(problem.initial), problem, limit)



def iterative_deepening_search(problem):
    for depth in range(sys.maxsize):
        result = depth_limited_search(problem, depth)
        if result != 'cutoff':
            return result