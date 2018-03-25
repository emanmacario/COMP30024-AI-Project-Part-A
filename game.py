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


        # Create the initial game state
        self.initial = GameState(to_move='O', utility=0, 
                        board=self.board,
                        moves=moves)


        # Print all moves for the initial state
        self.print_all_moves(self.initial)


        # Make a move
        new_state = self.result(self.initial, ((5,6),(6,6)))
        print(new_state.to_move)

  
        self.print_all_moves(new_state)
        self.display(new_state)
        

        print(self.is_surrounded((6,5), '@', new_state.board))
        




################################################################################
        
    # DEBUGGING FUNCTIONS

    def print_all_moves(self, state):
        """Print all moves for a player"""

        print("Printing all moves for '{:s}'".format(state.to_move))

        for start in sorted(list(state.moves)):
            print(start, state.moves[start])



################################################################################

    # PART A FUNCTIONS

    def print_legal_moves(self):
        """
        Prints the legal move counts for both the
        White player and Black player to standard output,
        in that order
        """

        white_moves = self.get_all_moves(self.board, 'O')
        black_moves = self.get_all_moves(self.board, '@')

        total_white_moves = 0
        total_black_moves = 0

        for start in white_moves:
            total_white_moves += len(white_moves[start])

        for start in black_moves:
            total_black_moves += len(black_moves[start])

        print(total_white_moves)
        print(total_black_moves)


################################################################################


    def actions(self, state):
        """Return all the legal moves for current state"""

        return state.moves



    def result(self, state, move):
        """Returns the result of a given action for a the current state"""

        # A move is a 2-tuple of 2-tuples E.g. ((1,2),(1,3))
        start, end = move

        # Illegal moves have no effect
        if start not in list(state.moves) or end not in state.moves[start]:
            print("Illegal move: {0} -> {1}".format(start, end))
            return state 


        # Create a copy of the board
        new_board = state.board.copy()

        # Make the move
        new_board[start] = '-'
        new_board[end] = state.to_move


        # Perform piece elimination after the move
        self.eliminate_pieces(end, new_board)


        # Get the next player to move, and all
        # the new possible moves for that player
        new_to_move = 'O' if state.to_move == '@' else '@'
        new_moves = self.get_all_moves(new_board, new_to_move)


        # Return the new gamestate
        return GameState(to_move=new_to_move, utility=0,
                         board=new_board, moves=new_moves)




    def eliminate_pieces(self, end, board):
        """Eliminates pieces on the board after a given
        move, taking into account the priority of the piece
        which just moved. Mutates the input board"""

        # Check each position in the board
        for point in sorted(list(board)):

            # Do not eliminate a priority piece in
            # the first iteration of eliminations
            if point == end:
                continue

            piece = board[point]

            # Only check the Black or White pieces
            if piece != '@' and piece != 'O':
                continue

            #print("'{0}' at {1}: {2}".format(piece, point, 
            #    self.is_surrounded(point, piece, board)))

            if self.is_surrounded(point, piece, board):
                board[point] = '-'


        # Finally, check if the priority piece is eliminated
        if self.is_surrounded(end, board[end], board):
            board[end] = '-'




    def is_surrounded(self, point, piece, board):
        """Returns true if a piece is surrounded horizontally
        or vertically by enemy pieces or corner squares"""

        # Get the enemy pieces. A corner square is considered
        # to be an enemy piece in this context, since it has
        # the ability to eliminate a piece
        enemy_pieces = ['@' if piece == 'O' else 'O', 'X']


        # Get all neighbouring pieces
        left  = board[self.get_new_point(point, self.DIRECTION_LEFT)]
        right = board[self.get_new_point(point, self.DIRECTION_RIGHT)]
        up    = board[self.get_new_point(point, self.DIRECTION_UP)]
        down  = board[self.get_new_point(point, self.DIRECTION_DOWN)]


        # Return true if a piece should be eliminated, else return false
        if (left in enemy_pieces and right in enemy_pieces) or \
            (up in enemy_pieces and down in enemy_pieces):

            return True

        return False



    def utility(self, state, player):
        """Returns a utility value for a player,
        given the current state"""
        pass



    def terminal_test(self, state):
        """A state is terminal if it is won or
        has resulted in a tie"""

        white_pieces = 0
        black_pieces = 0

        # Might need to do list(state.board) to avoid bugs
        for point in state.board:
            if state.board[point] == '@':
                black_pieces += 1
            elif state.board[point] == 'O':
                white_pieces += 1   


        # The state is terminal if black or white has less than
        # two pieces on the board
        if white_pieces < 2 or black_pieces < 2:
            return True

        return False



    def get_all_moves(self, board, player):
        """All possible moves for a player, as a dictionary
        of tuples (start points), to lists of tuples (possible
        end point)"""


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




    def display(self, state):
        """Print or otherwise display the state
        of the current board configuration"""

        board = state.board
        board_repr = ""

        for i in range(self.size):
            for j in range(self.size):
                board_repr += (board[(j,i)] + ' ')

            board_repr += "\n" 

        print(board_repr)


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
