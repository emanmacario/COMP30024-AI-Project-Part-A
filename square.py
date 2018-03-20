'''
This file contains the Square class
that represents a space on the Board
in the game 'Watch Your Back!'
'''
class Square:
    def __init__(self, row, col, state):
        self.row = row
        self.col = col
        self.state = state
