import numpy as np
import pygame

ROW = 6
COLOUMN = 7


def create_board():
    board = np.zeros((ROW, COLOUMN))
    return board


def drop_piece(board, row, col, piece):
    board[row, col] = piece


def is_valid_location(board, col):
    return board[0, col] == 0


def get_next_open_row(board, col):
    for row in range(ROW-1, 0, -1):  # 5->0
        if board[row, col] == 0:
            return row
    return 0


def print_board():
    pass


def winning_move(board, piece):
    # check horizontal
    for col in range(COLOUMN-3):
        for row in range(ROW):
            if (board[row, col] == piece and board[row, col+1] == piece
               and board[row, col+2] == piece and board[row, col+3] == piece):
                return True
    # check vertical
    for col in range(COLOUMN):
        for row in range(ROW-3):
            if (board[row, col] == piece and board[row+1, col] == piece
               and board[row+2, col] == piece and board[row+3, col] == piece):
                return True
    # check neg slope
    for col in range(COLOUMN-3):
        for row in range(ROW-3):
            if (board[row, col] == piece
                    and board[row+1, col+1] == piece
                    and board[row+2, col+2] == piece
                    and board[row+3, col+3] == piece):
                return True
    # check pos slope
    for col in range(COLOUMN-3):
        for row in range(ROW-1, ROW-4, -1):
            if (board[row, col] == piece
                    and board[row-1, col+1] == piece
                    and board[row-2, col+2] == piece
                    and board[row-3, col+3] == piece):
                return True
    return False


def draw_board():
    pass


board = create_board()
print(board)
game_over = False
turn = 0
pygame.init()
SQUARESIZE = 100
width = COLOUMN*SQUARESIZE
height = (ROW+1)*SQUARESIZE
size = (width, height)
# screen = pygame.display.set_mode(size)

while not game_over:
    if turn == 0:
        col = int(input('Player 1 (0-6): '))
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            print(f'debug 1: {row}, {col}')
            drop_piece(board, row, col, 1)
            print(board)
            if winning_move(board, 1):
                print('Player 1 wins')
                game_over = True
        else:
            print('Player 1: not valid move')
    else:
        col = int(input('Player 2 (0-6): '))
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            print(f'debug 2: {row}, {col}')
            drop_piece(board, row, col, 2)
            print(board)
            if winning_move(board, 1):
                print('Player 1 wins')
                game_over = True
        else:
            print('Player 2: not valid move')

    turn += 1
    turn = turn % 2
