"""
Game class
"""

from board import *

from collections import namedtuple
from collections import defaultdict


GameState = namedtuple('GameState', 'to_move, utility, board, moves')



class Game:

    """An abstract game type"""

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

    # Possible directions of movement
    DIRECTION_UP    = "UP"
    DIRECTION_DOWN  = "DOWN"
    DIRECTION_LEFT  = "LEFT"
    DIRECTION_RIGHT = "RIGHT"

    # Possible pieces
    SQUARE_EMPTY  = '-'
    SQUARE_CORNER = 'X'
    SQUARE_BLACK  = '@'
    SQUARE_WHITE  = 'O'



    def __init__(self, board_config=None, size=8):
        self.size = 8
        self.board = self.init_board(board_config)


        # print board state
        print(self.__repr__())

        # Get the moves for a player
        moves = self.get_all_moves(self.board, 'O')


        # Print all moves for a player
        print("Printing all moves for '{:s}'".format('O'))
        for start in sorted(list(moves)):
            print(start, moves[start])


        # Create the initial game state
        self.initial = GameState(to_move='O', utility=0, 
                        board=self.board,
                        moves=moves)

        # print(self.is_legal_move((5,3), self.DIRECTION_LEFT, 'O'))
        



    def actions(self, state):
        """Return all the legal moves for current state"""

        return state.moves



    def get_all_moves(self, board, player):
        """All possible moves for a player"""


        directions = [self.DIRECTION_DOWN, self.DIRECTION_LEFT,
                      self.DIRECTION_RIGHT, self.DIRECTION_UP]

        all_moves = defaultdict(list)

        for point in list(board):
            if board[point] == player:
                for direction in directions:

                    if self.is_legal_move(point, direction, player):
                        new_valid_point = self.get_valid_point(point, direction)

                        all_moves[point].append(new_valid_point)


                
        return all_moves
    


    def init_board(self, board_config):
        """Initialise the board from the input
        board configuration, where the board is
        a dictionary of tuple keys to character
        values (pieces). E.g. {(1,2):'X'}
        """

        board = defaultdict(str)

        for row in range(self.size):
            for column in range(self.size):

                char = board_config[row][column] 

                board[(column, row)] = char

        return board



    def result(self, state, move):
        """Returns the result of a given action for a the current state"""



    def display(self, state):
        """Print or otherwise display the state
        of the current board configuration"""
        print(state.board.__repr__())



    def is_legal_move(self, start, direction, player):
        """Returns if a move is legal, given a starting
        point, and a direction"""

        # First check to see if the player has a piece on that
        # square.
        if self.board[start] != player:
            return False

        # Calculate new possible points
        new_point = self.get_new_point(start, direction)
        jump_point = self.get_new_point(new_point, direction)
        
        if self.is_square_open(new_point) or self.is_square_open(jump_point):
            return True

        return False



    def is_square_open(self, point):
        """A square is open if the there is no opponent
        piece on it, and it is not a corner square."""

        return self.board[point] == '-'



    def get_new_point(self, start, direction):
        """Calculates the new square position given
        a starting square position and a direction.
        Returns point as a 2-tuple: (column, row)
        """

        # Get the starting row and column numbers
        column, row = start

        # Calculate the new co-ordinates of square, given the direction
        if direction == self.DIRECTION_DOWN:
            row += 1
        elif direction == self.DIRECTION_UP:
            row -= 1
        elif direction == self.DIRECTION_LEFT:
            column -= 1
        else:
            column += 1
        
        return (column, row)



    def get_valid_point(self, start, direction):
        """Returns the new point of a piece after
        making a valid move"""

        # Calculate new possible points
        new_point = self.get_new_point(start, direction)
        jump_point = self.get_new_point(new_point, direction)
        
        if self.is_square_open(new_point):
            return new_point

        return jump_point



    def __repr__(self):
        """Representation of the board state,
        exact same as the input configuration
        given in the spec"""

        board_repr = ""

        for i in range(self.size):
            for j in range(self.size):
                board_repr += (self.board[(j,i)] + ' ')

            board_repr += "\n" 

        return board_repr
