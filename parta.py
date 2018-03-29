"""
COMP30024 Artificial Intelligence - Project Part A
Semester 1, 2018.

Created by Emmanuel Macario and James Marshall
Student Numbers: Emmanuel - 831659, James - 728089
"""

from game import *


def parse_input():
    """
    Reads in a board configuration from
    the standard input, as well as the method
    of analysis of the board. Creates a nested
    list representation of the board, and returns
    both the method and configuration.
    """

    # The total number of lines to be inputted
    TOTAL_LINES = 9

    # The board configuration, stored as a
    # two dimensional list of characters
    board_config = []

    # Read in each row, one by one
    for _ in range(TOTAL_LINES-1):
        row = input().rstrip('\r').split(' ')
        board_config.append(row)


    # Read in the method of analysis
    method = input()

    return method, board_config



def main():
    """
    Main driver program for Part A, controlling the flow of execution.
    """

    # Parse the input data, getting the
    # board configuration and the method of analysis
    method, board_config = parse_input()


    # Create a new board, based on the given board configuration
    game = WatchYourBack(board_config)


    # Based on the method of analysis, print the results
    if method == "Moves":
        game.print_legal_moves()
    else:
        game.print_legal_move_sequence()



# Runs the main program.
if __name__ == "__main__":
    main()