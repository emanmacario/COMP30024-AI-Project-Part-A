'''
This file contains the Board class,
which represents the entire game board.
'''

class Board:
    """
    A 'Watch Your Back!' game board, used for
    storing the state of the game, and trying
    out different scenarios.
    """

    # Class variables
    WIDTH = 8
    HEIGHT = 8


    def __init__(self, width, height):
        """
        Board constructor. Takes as input the width
        and height of the game board.
        """
        self.width = width
        self.height = height
        self.grid = [[] for _ in range(WIDTH)]
        self.curr_rows = 0



    def total_pieces(self):
        """
        Counts the total number of pieces
        on the board.
        """
        pass


    def add_row(self, row):
        """
        Adds a row to the board if it is possible.
        """
        grid[rows] = row
        row += 1



    @classmethod
    def from_str(cls, row_str):
        """
        Takes a string representing one row
        of the game board, and parses it into a list
        representation.
        """

        # Obtain a new row
        row = row_str.rstrip('\r').split(' ')

        return row



