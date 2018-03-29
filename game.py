"""
COMP30024 Artificial Intelligence - Project Part A
Semester 1, 2018.

Created by Emmanuel Macario and James Marshall
Student Numbers: Emmanuel - 831659, James - 728089

This code has taken inspiration from source code contained in the AIMA 
Python GitHub repository (https://github.com/aimacode/aima-python).
"""

from collections import namedtuple
from collections import defaultdict
from search import *
import copy



# A gamestate includes the player to move, a list of possible moves in the form 
# of a dictionary {(x,y): [(x1,y1)...(xn,yn)]}, a board in the form of a 
# dictionary {(x,y): SQUARE_VALUE} , and a pieces dictionary, which maintains 
# and keeps track of the locations of both players' pieces, in the same fashion 
# as the board dictionary.
GameState = namedtuple('GameState', 'to_move, board, pieces, moves')



class WatchYourBack():

    """
    This class represents a game of 'Watch Your Back!' on an 
    8 x 8 board, with the White player playing 'O', and the Black
    player playing '@'.
    """

    # Possible directions of movement
    DIRECTION_UP    = "UP"
    DIRECTION_DOWN  = "DOWN"
    DIRECTION_LEFT  = "LEFT"
    DIRECTION_RIGHT = "RIGHT"

    # Possible square values
    SQUARE_EMPTY  = '-'
    SQUARE_CORNER = 'X'
    SQUARE_BLACK  = '@'
    SQUARE_WHITE  = 'O'


    def __init__(self, board_config=None, size=8):
        """
        Initialise a new game of 'Watch Your Back!'
        """

        # Set the size of the board.
        self.size = size

        # Initialise the board and pieces dictionaries
        # to add to the initial gamestate tuple.
        board = self.init_board(board_config)
        pieces = self.init_pieces(board)
        

        # Get the possible moves for the White player, 
        # given the input board configuration.
        moves = self.get_all_moves(board, self.SQUARE_WHITE, pieces)


        # Create and set the initial gamestate.
        self.initial = GameState(to_move=self.SQUARE_WHITE,
                                 board=board, 
                                 moves=moves, 
                                 pieces=pieces)


    
    def init_board(self, board_config):
        """
        Initialise the board from the input
        board configuration, where the board is
        a dictionary of tuple keys to square
        values. E.g. {(1,2):'@', {(0,7):'X', ...., etc}
        """

        board = defaultdict(str)

        for row in range(self.size):
            for column in range(self.size):
                char = board_config[row][column] 
                board[(column, row)] = char

        return board



    def init_pieces(self, board):
        """
        Initialise the pieces dictionary from
        the initial board, where pieces is a
        dictionary of tuple keys to player
        character values. E.g. {(1,2):'O', (1,3):'@'}
        """

        pieces = defaultdict(str)

        for point in board:

            if board[point] == self.SQUARE_WHITE or \
                    board[point] == self.SQUARE_BLACK:

                pieces[point] = board[point]

        return pieces



    def actions(self, state):
        """
        Return all the legal moves for current game state.
        """

        possible_moves = []

        for start in state.moves:
            for end in state.moves[start]:
                possible_moves.append((start,end))

        return possible_moves



    def result(self, state, move):
        """
        Returns the new gamestate after a move 
        has been made in the current gamestate.
        """

        # A move is a 2-tuple of 2-tuples E.g. ((1,2),(1,3)).
        # The first tuple indicates the starting position, and
        # the second tuple indicates the end position.
        start, end = move


        # Illegal moves have no effect.
        if start not in list(state.moves) or end not in state.moves[start]:
            print("Illegal move: {0} -> {1}".format(start, end))
            return copy.deepcopy(state)


        # Before making a move, create copies
        # of the board and pieces dictionaries.
        new_board = state.board.copy()
        new_pieces = state.pieces.copy()


        # Make the move, updating the new dictionaries.
        new_board[start] = self.SQUARE_EMPTY
        new_board[end] = state.to_move

        del new_pieces[start]
        new_pieces[end] = state.to_move


        # Perform piece elimination after the move, 
        # giving the newly moved piece elimination priority.
        self.eliminate_pieces(end, new_board, new_pieces)


        # In part A, the White player will always be the next to move.
        new_to_move = self.SQUARE_WHITE


        # Get all the new possible moves for the White 
        # player, once their original move has been made.
        new_moves = self.get_all_moves(new_board, new_to_move, new_pieces)


        # Create and return the new gamestate.
        return GameState(to_move=new_to_move,
                         board=new_board, 
                         moves=new_moves, 
                         pieces=new_pieces)



    def terminal_test(self, state):
        """
        Tests whether a given gamestate is terminal. 
        For the purpose of Part A, a state is considered 
        to be terminal if all Black pieces are eliminated.
        """

        total_black_pieces = 0

        # Might need to do list(state.board) to avoid bugs
        for point in state.pieces:
            if state.pieces[point] == self.SQUARE_BLACK:
                total_black_pieces += 1

        if total_black_pieces == 0:
            return True

        return False



    def display(self, state):
        """
        Prints or otherwise displays current
        board configuration for a given gamestate.
        """

        board = state.board
        board_repr = ""

        for i in range(self.size):
            for j in range(self.size):
                board_repr += (board[(j,i)] + ' ')

            board_repr += "\n" 

        print(board_repr)



    def print_legal_moves(self):
        """
        Prints the legal move counts for both the
        White player and Black player to standard output,
        in that order
        """
        board = self.initial.board
        pieces = self.initial.pieces

        white_moves = self.get_all_moves(board, self.SQUARE_WHITE, pieces)
        black_moves = self.get_all_moves(board, self.SQUARE_BLACK, pieces)

        total_white_moves = 0
        total_black_moves = 0

        for start in white_moves:
            total_white_moves += len(white_moves[start])

        for start in black_moves:
            total_black_moves += len(black_moves[start])

        print(total_white_moves)
        print(total_black_moves)



    def get_legal_move_sequence(self):
        """
        Prints a sequence of legal moves for the White
        player that would lead all black pieces being 
        eliminated, to the standard output.
        """

        # Assume that we will always be given an input
        # board configuration where we can reach a terminal
        # state.
        terminal_node = iterative_deepening_search(self)

        moves = terminal_node.solution()

        for (start, end) in moves:
            print("{0} -> {1}".format(start, end))
        


    def eliminate_pieces(self, end, board, pieces):
        """
        Eliminates pieces on the board after a given
        move, taking into account the priority of the piece
        that just moved. Mutates the input board during the
        process.
        """

        # Need to check each piece on the board.
        for point in list(pieces):

            # Do not eliminate a priority piece in
            # the first iteration of eliminations
            if point == end:
                continue

            piece = pieces[point]

            # If a piece is surrounded, remove
            # the piece from the board.
            if self.is_surrounded(point, piece, board):
                board[point] = self.SQUARE_EMPTY
                del pieces[point]


        # Finally, check if the priority piece is eliminated
        if self.is_surrounded(end, board[end], board):
            board[end] = self.SQUARE_EMPTY
            del pieces[end]



    def is_surrounded(self, point, piece, board):
        """
        Returns true if a piece is surrounded horizontally
        or vertically by enemy pieces or corner squares, and
        hence, should be eliminated.
        """

        # Get the enemy pieces. A corner square is considered
        # to be an enemy piece in this context, since it has
        # the ability to eliminate either Black or White pieces.
        enemy_pieces = [self.SQUARE_BLACK if piece == self.SQUARE_WHITE else \
                        self.SQUARE_WHITE, self.SQUARE_CORNER]


        # Get the horizontally neighbouring pieces.
        left  = board.get(self.get_new_point(point, self.DIRECTION_LEFT), '')
        right = board.get(self.get_new_point(point, self.DIRECTION_RIGHT), '')

        # Check if the player's piece is horizontally surrounded.
        if left in enemy_pieces and right in enemy_pieces:
            return True


        # Get the vertically neighbouring pieces.
        up   = board.get(self.get_new_point(point, self.DIRECTION_UP), '')
        down = board.get(self.get_new_point(point, self.DIRECTION_DOWN), '')

        # Check if the player's piece is vertically surrounded.
        if up in enemy_pieces and down in enemy_pieces:
            return True

        return False



    def get_all_moves(self, board, player, pieces):
        """
        Enumerates and returns all possible moves for 
        a player, given a board configuration.
        """

        # Note that directions have been placed purposefully in this
        # order so that moves can be inserted in order in the list.
        # This avoids the overhead of sorting, which is needed for
        # direct comparison of gamestates.
        directions = [self.DIRECTION_LEFT, self.DIRECTION_UP,
                      self.DIRECTION_DOWN, self.DIRECTION_RIGHT]

        all_moves = defaultdict(list)

        for start in list(pieces):
            if pieces[start] == player:
                for direction in directions:
                    move = self.get_legal_move(board, start, direction, player)
                    if move:
                        all_moves[start].append(move)

        return all_moves
    


    
    def get_legal_move(self, board, start, direction, player):
        """
        Returns a legal move (end point) given a player, starting 
        point, and direction. If there is no available move, returns
        False.
        """

        # First check to see if the player actually
        # has a piece on the starting square.
        if board[start] != player:
            return False


        # Get coordinates of the two possible end points,
        # one for a normal move, and one for a jump. 
        new_point = self.get_new_point(start, direction)
        jump_point = self.get_new_point(new_point, direction)
        

        # Return the destination point for a 
        # valid move, otherwise return False.
        if self.is_square_open(board, new_point):
            return new_point
        elif self.is_square_open(board, jump_point):
            return jump_point

        return False



    def is_square_open(self, board, point):
        """
        A square is open if the there is no opponent
        piece on it, and it is not a corner square.
        """

        if not board.get(point, ''):
            return False

        return board[point] == self.SQUARE_EMPTY



    def get_new_point(self, start, direction):
        """
        Calculates the new square position given
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