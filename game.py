"""
Game class
"""

from search import *

from collections import namedtuple
from collections import defaultdict
import copy


GameState = namedtuple('GameState', 'to_move, utility, board, moves, pieces')



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
        self.size = size
        self.board = self.init_board(board_config)
        self.pieces = self.init_pieces(self.board)
        

        # Get the moves for a player
        moves = self.get_all_moves(self.board, self.SQUARE_WHITE, self.pieces)


        # Create the initial game state
        self.initial = GameState(to_move=self.SQUARE_WHITE, utility=0, 
                        board=self.board, moves=moves, pieces=self.pieces)


        """
        self.print_all_moves(self.initial)

        new_state = self.result(self.initial, (((5,2),(6,2))))

        newer_state = self.result(new_state, ((6,2),(5,2)))

        print("Does comparing states work?")
        print("Initial state:")
        print(self.initial.to_move == newer_state.to_move)
        print(self.initial.utility == newer_state.utility)
        print(self.initial.board == newer_state.board)
        print(self.initial.moves == newer_state.moves)
        print(self.initial.pieces == newer_state.pieces)


        print()
        for i in range(8):
            for j in range(8):
                point = (i, j)

                if self.initial.board[point] != newer_state.board[point]:
                    print("Point:", point)
                    print("At initial board: ", self.initial.board[point])
                    print("At newer board:   ", newer_state.board[point])

        print(sorted(self.initial.board.keys()))
        print(sorted(newer_state.board.keys()))
        """




    def init_pieces(self, board):

        pieces = defaultdict(str)

        for point in board:

            if board[point] == self.SQUARE_WHITE or \
                    board[point] == self.SQUARE_BLACK:

                pieces[point] = board[point]

        return pieces

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

        white_moves = self.get_all_moves(self.board, 'O', self.pieces)
        black_moves = self.get_all_moves(self.board, '@', self.pieces)

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
        terminal_node = iterative_deepening_search(self)

        if terminal_node is None:
            print("You fucked up son. No solution!")
            return

        """
        print("Final state")
        self.display(terminal_node.state)


        print("Printing board states leading to elimination")
        for node in terminal_node.path():
            self.display(node.state)
        """

        
        moves = terminal_node.solution()

        print("Printing moves leading to elimination")
        for (start, end) in moves:
            print("{0} -> {1}".format(start, end))
        

        


################################################################################


    def actions(self, state):
        """Return all the legal moves for current game
        state as a list of 2-tuple of 2-tuples.
        E.g [((x1,y1),(x2,y2)), ..., ...]
        """

        possible_moves = []

        for start in state.moves:
            for end in state.moves[start]:
                possible_moves.append((start,end))

        return possible_moves



    def result(self, state, move):
        """Returns the result of a given action for a the current state"""

        # A move is a 2-tuple of 2-tuples E.g. ((1,2),(1,3))
        start, end = move

        # Illegal moves have no effect
        if start not in list(state.moves) or end not in state.moves[start]:
            print("Illegal move: {0} -> {1}".format(start, end))
            return copy.deepcopy(state)


        # Create a copy of the board
        new_board = state.board.copy()
        new_pieces = state.pieces.copy()


        # Make the move, updating the board and pieces data structures
        new_board[start] = '-'
        new_board[end] = state.to_move

        del new_pieces[start]
        new_pieces[end] = state.to_move


        # Perform piece elimination after the move, 
        # giving the newly moved piece elimination priority.
        self.eliminate_pieces(end, new_board, new_pieces)


        # Get the next player to move, and all
        # the new possible moves for that player
        # new_to_move = 'O' if state.to_move == '@' else '@'
        # In part A, only White will move
        new_to_move = 'O'

        new_moves = self.get_all_moves(new_board, new_to_move, new_pieces)

        # Return the new gamestate
        return GameState(to_move=new_to_move, utility=0,
                         board=new_board, moves=new_moves, pieces=new_pieces)




    def eliminate_pieces(self, end, board, pieces):
        """Eliminates pieces on the board after a given
        move, taking into account the priority of the piece
        which just moved. Mutates the input board"""

        # Check each position in the board
        for point in list(pieces):

            # Do not eliminate a priority piece in
            # the first iteration of eliminations
            if point == end:
                continue

            piece = pieces[point]


            # If a piece is surrounded, remove
            # the piece from the board.
            if self.is_surrounded(point, piece, board):
                board[point] = '-'
                pieces[point] = '-'


        # Finally, check if the priority piece is eliminated
        if self.is_surrounded(end, board[end], board):
            board[end] = '-'
            del pieces[end]




    def is_surrounded(self, point, piece, board):
        """Returns true if a piece is surrounded horizontally
        or vertically by enemy pieces or corner squares"""

        # Get the enemy pieces. A corner square is considered
        # to be an enemy piece in this context, since it has
        # the ability to eliminate either Black or White pieces.
        enemy_pieces = ['@' if piece == 'O' else 'O', 'X']


        # Get all neighbouring pieces
        left  = board.get(self.get_new_point(point, self.DIRECTION_LEFT), '')
        right = board.get(self.get_new_point(point, self.DIRECTION_RIGHT), '')

        if left in enemy_pieces and right in enemy_pieces:
            return True


        up    = board.get(self.get_new_point(point, self.DIRECTION_UP), '')
        down  = board.get(self.get_new_point(point, self.DIRECTION_DOWN), '')

        if up in enemy_pieces and down in enemy_pieces:
            return True


        return False



    def utility(self, state, player):
        """Returns a utility value for a player,
        given the current state"""
        pass



    def terminal_test(self, state):
        """
        Tests whether a state is terminal. For
        the purpose of Part A, a state is considered terminal
        if all Black pieces are eliminated. In a real
        game, however, a state is terminal if there are
        less than 2 remaining pieces for either player.
        """

        black_pieces = 0

        # Might need to do list(state.board) to avoid bugs
        for point in state.pieces:
            if state.pieces[point] == '@':
                black_pieces += 1

        if black_pieces == 0:
            return True

        return False



    def get_all_moves(self, board, player, pieces):
        """All possible moves for a player, as a dictionary
        of tuples (start points), to lists of tuples (possible
        end point)"""

        # Note that directions have been placed purposefully in this
        # order such that moves can be inserted in order to a list.
        # This avoids the overhead of sorting.
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



    def get_legal_move(self, board, start, direction, player):
        """Returns a legal move given a player, starting point,
        and direction. If there is no available move, returns
        False."""

        # First check to see if the player has a piece on that
        # square.
        if board[start] != player:
            return False

        # Calculate new possible points
        new_point = self.get_new_point(start, direction)
        jump_point = self.get_new_point(new_point, direction)
        

        # Return end point if a move is valid
        if self.is_square_open(board, new_point):
            return new_point
        elif self.is_square_open(board, jump_point):
            return jump_point

        return False



    def is_square_open(self, board, point):
        """A square is open if the there is no opponent
        piece on it, and it is not a corner square."""

        if not board.get(point, ''):
            return False

        return board[point] == '-'



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
