"""
Game class
"""

from board import *

from collections import namedtuple
from collections import defaultdict


GameState = namedtuple('GameState', 'to_move, utility, board, moves')



class Game:


    def actions(self, state):
        """Return a list of the allowable moves at this point"""
        raise NotImplementedError


    def result(self, state, move):
        """Return the state that results from making a move from the state"""
        raise NotImplementedError


    def utility(self, state, player):
        """Returns the utility value of a terminal state to the player"""
        raise NotImplementedError


    def terminal_test(self, state):
        """Returns True if this is a final state for the game"""
        raise NotImplementedError


    def to_move(self, state):
        """Return the player whose move it is in the current game state"""
        return state.to_move


    def display(self, state):
        """Print or otherwise display the state"""
        print(state)


    def play_game(self, *players):
        """Play an n-person, move alternating game"""
        state = self.initial

        while True:
            for player in players:
                move = player(self, state)
                state = self.result(state, move)
                if self.terminal_test(state):
                    self.display(state)
                    return self.utility(state, self.to_move(self.initial))





class WatchYourBack(Game):

    """Play Watch Your Back! on an 8 x 8 board with White
    (first player) playing 'O', and Black (second player)
    playing '@'. A state has the player to move, a cached
    utility, a list of moves in the form of a dictionary
    {(x,y): [(x1,y1)...(xn,yn)]}, and a board, in the form
    of a dict of {(x, y): Player} entries, where Player is 
    'X' or 'O'
    """


    def __init__(self, board_config=None):
        self.board = Board(board_config)
        self.initial = GameState(to_move='O', 
                                 utility=0, 
                                 board=self.board.__repr__(), 
                                 moves=defaultdict(list))


    def actions(self, state):
        """Return all the legal moves for a given player"""

        # Get the player to move
        player = state.to_move

        return state.moves


    def result(self, state, move):
        if move not in state.moves:
            return state
