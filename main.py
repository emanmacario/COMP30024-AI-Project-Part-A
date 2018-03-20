from board import *


def parse_input(board):
    """
    Reads in a board configuration from
    the standard input, as well as the method
    of analysis of the board. Updates the game
    board and returns the method of analysis.
    """

    # The total number of lines to be inputted
    TOTAL_LINES = 9

    # Read in each row, one by one
    for _ in range(TOTAL_LINES-1):
        row = Board.from_str(input())
        print(row)

    # Read in the method of analysis
    method = input()
    print(method)

    return method



def main():
    """
    Main program, controlling the flow of execution.
    """

    # Create a new board.
    board = Board(Board.WIDTH, Board.HEIGHT)

    # Parse the input data, and update the board.
    parse_input(board)



# Runs the main program.
if __name__ == "__main__":
    main()