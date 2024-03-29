"""
COMP30024 Artificial Intelligence - Project Part A
Semester 1, 2018.

Adapted by Emmanuel Macario and James Marshall
Student Numbers: Emmanuel - 831659, James - 728089

This code has been modified from source code contained in the AIMA 
Python GitHub repository (https://github.com/aimacode/aima-python),
for Part A of the project.
"""

import sys


class Node:

    """
    A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state.  Also includes the action that got us to this state, and
    the total path_cost (also known as g) to reach the node.
    """

    def __init__(self, state, parent=None, action=None, path_cost=None):
        """Creates a node in a search tree"""
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0

        if parent:
            self.depth = parent.depth + 1



    def child_node(self, game, action):
        """Create a new child node from this node, by applying
        a certain action to the current state"""
        next_state = game.result(self.state, action)

        return Node(next_state, self, action)



    def expand(self, game):
        """List the nodes reachable in one step from this node"""
        return [self.child_node(game, action)
                    for action in game.actions(self.state)]



    def solution(self):
        """Return the sequence of actions to go from the root
        to this node. Since the root node does not have an
        action, skip it"""
        return [node.action for node in self.path()[1:]]



    def path(self, reverse=True):
        """
        Return a list of nodes forming the path from the root to this node.
        If the reversed flag is set to False, gets the path from node to root
        instead.
        """

        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent

        if reverse:
            return list(reversed(path_back))

        return path_back


    def __eq__(self, other):
        """Returns True if one node is equal to the other"""
        return isinstance(other, Node) and self.state == other.state




def depth_limited_search(game, limit):
    """
    Perform depth limited search, on a state 
    space, given a certain depth limit.
    """

    def recursive_dls(node, game, limit):
        if game.terminal_test(node.state):
            return node
        elif limit == 0:
            return 'cutoff'
        else:
    
            cutoff_occurred = False
            path = node.path(reverse=False)

            for child in node.expand(game):

                # Do not explore already explored states
                if child in path:
                    continue
                
                result = recursive_dls(child, game, limit-1)
                if result == 'cutoff':
                    cutoff_occurred = True
                elif result is not None:
                    return result
            return 'cutoff' if cutoff_occurred else None


    # Body of depth-limited search
    return recursive_dls(Node(game.initial), game, limit)



def iterative_deepening_search(game):
    """
    Perform iterative deepening search on
    a state space for a given instance of
    the game 'Watch Your Back!'
    """
    for depth in range(sys.maxsize):
        result = depth_limited_search(game, depth)
        if result != 'cutoff':
            return result