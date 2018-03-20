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

    def isValidMove(piece, direction):
        '''
        Gets given a piece and its inteded
        direction of movement and decides whether
        the move would be legal.
        '''


    def move(piece, direction):
        '''
        Moves a given piece in a given direction
        if the move has already been checked as being
        legal.
        '''


    def checkWinner():
        '''
        Checks the board to see if either player
        has officially won the game.
        Returns the Player object if that player
        has won.
        '''


    def checkKill():
        '''
        Checks the game board to see if any piece
        is in a position where it is eliminated.
        Returns the row and column of a piece if it
        needs to be eliminated.
        '''
