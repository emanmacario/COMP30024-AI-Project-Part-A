"""
This file contains the Square class that represents a
square on the game board.
"""

class Square:

    def __init__(self, row, column, char):
        """Square constructor"""
        self.row = row
        self.column = column
        self.char = char
        self.priority = False
        self.neighbours = {}  # A dictionary of neighbouring squares


    def get_position(self):
        """Return the position of a square as a 2-tuple
        in the form (column, row)"""
        return (self.column, self.row)


    def set_neighbour(self, direction, square):
        """Sets the neighbour of a square, assigning
        it a unique direction as a key"""
        self.neighbours[direction] = square


    def get_neighbour(self, direction):
        """Returns the neighbour of a square, in a given
        direction"""
        return self.neighbours[direction]


    def get_all_neighbours(self):
        """Returns the dictionary of neighbouring squares"""
        return self.neighbours


    def print_all_neighbours(self):
        """Prints all the neighbours of this square"""
        print("({:d},{:d})".format(self.column, self.row))
        print(self.neighbours)


    def __repr__(self):
        """Representation of a square"""
        return self.char + " "