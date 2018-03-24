'''
This file contains the Board class,
which represents the entire game board.
'''

from square import *
from collections import defaultdict


class Board:
    """
    A game board for 'Watch Your Back!', used for
    storing the state of the game, and trying
    out different scenarios.
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


    def __init__(self, board_config=None, width=8, height=8):
        """
        Board constructor. Takes as input the width
        and height of the game board.
        """
        self.width = width
        self.height = height
        self.squares = [[] for _ in range(width)]

        if (board_config):
            self.fill_board(board_config)

        self.set_all_neighbours()

        # Print the board configuration
        print(self)

        # Prints all possible moves for every piece on the board
        #self.print_all_possible_moves(self.SQUARE_WHITE)
        #self.print_all_possible_moves(self.SQUARE_BLACK)

        

    def print_all_possible_moves(self, char):
        """For all pieces on the board, prints all possible moves"""

        total = 0

        for i in range(self.height):
            for j in range(self.width):
                piece = self.squares[i][j].char

                if piece != char:
                    continue
                
                print("Piece: '{:s}' at ({:d},{:d})".format(piece,j,i))

                can_move = self.is_valid_move(self.DIRECTION_UP, i, j)
                if (can_move):
                    print(self.DIRECTION_UP)
                    total += 1

                
                can_move = self.is_valid_move(self.DIRECTION_RIGHT, i, j)
                if (can_move):
                    print(self.DIRECTION_RIGHT)
                    total += 1


                can_move = self.is_valid_move(self.DIRECTION_DOWN, i, j)
                if can_move:
                    print(self.DIRECTION_DOWN)
                    total += 1


                can_move = self.is_valid_move(self.DIRECTION_LEFT, i, j)
                if can_move:
                    print(self.DIRECTION_LEFT)
                    total += 1
            print("\n")

        print("Total possible moves for '{:s}': {:d}".format(char, total))



                

    def fill_board(self, board_config):
        """Fills in the board with squares"""

        for row in range(self.height):
            for column in range(self.width):
                char = board_config[row][column]
                self.squares[row].append(Square(row, column, char))



    def set_neighbours(self, row, column):
        """Sets the neighbours for a given square"""
        if row != 0:
            self.squares[row][column].set_neighbour(Board.DIRECTION_UP,
                self.squares[row-1][column])

        if column != 0:
            self.squares[row][column].set_neighbour(Board.DIRECTION_LEFT,
                self.squares[row][column-1])

        if row != self.width-1:
            self.squares[row][column].set_neighbour(Board.DIRECTION_DOWN,
                self.squares[row+1][column])

        if column != self.height-1:
            self.squares[row][column].set_neighbour(Board.DIRECTION_RIGHT,
                self.squares[row][column+1])



    def set_all_neighbours(self):
        """Sets the neighbours for all squares on the board"""
        for row in range(self.height):
            for column in range(self.width):
                self.set_neighbours(row, column)



    def make_move(self, row, column):
        """
        Makes a valid move for a given piece.
        """





    def is_valid_move(self, direction, row, column):
        """
        Returns True if a move is valid, else returns False.
        The row and column number is of the piece to be moved,
        and the direction indicates the direction to be moved.
        """

        # Get the originating square and possible piece
        square = self.squares[row][column]
        piece = square.char

        # First check that the certain piece on a square 
        # we are trying to move actually exists.
        if piece == self.SQUARE_EMPTY or piece == self.SQUARE_CORNER:
            return False

        # Calculate the new co-ordinates of the piece, given the direction
        if direction == self.DIRECTION_DOWN:
            row += 1
        elif direction == self.DIRECTION_UP:
            row -= 1
        elif direction == self.DIRECTION_LEFT:
            column -= 1
        else:
            column += 1

        # Check if the move is inside the bounds of the board
        if row < 0 or row > self.height-1 or column < 0 or column > self.width-1:
            return False

        # If the square is empty, it is a valid move
        if self.squares[row][column].char == self.SQUARE_EMPTY:
            return True


        # Otherwise, check if we can perform a 'jump'
        if direction == self.DIRECTION_DOWN:
            row += 1
        elif direction == self.DIRECTION_UP:
            row -= 1
        elif direction == self.DIRECTION_LEFT:
            column -= 1
        else:
            column += 1

        # Check if the move is inside the bounds of the board
        if row < 0 or row > self.height-1 or column < 0 or column > self.width-1:
            return False


        # If the square is empty, it is a valid move
        if self.squares[row][column].char == self.SQUARE_EMPTY:
            return True

        return False



    def __str__(self):
        """Representation of the current board,
        used for visualisation by the players"""
        board_repr = ""

        for row in self.squares:
            for square in row:
                board_repr += square.__repr__()
            board_repr += "\n"

        return board_repr



    def __repr__(self):
        """Representation of the current board,
        used to represent the board as a dictionary
        of tuples to pieces

        i.e. {(x,y):'X'}
        """
        s = defaultdict(str)

        for i in range(8):
            for j in range(8):
                square = self.squares[i][j]

                if square.char != self.SQUARE_EMPTY:    
                    s[(j,i)] = square.char

        return s

