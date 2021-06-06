import numpy as np
from numpy.core.fromnumeric import squeeze
import pygame
import sys
import math

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
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


def draw_board(board):
    for col in range(COLOUMN):
        for row in range(ROW):
            pygame.draw.rect(screen, BLUE, (col*SQUARESIZE, row*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))  # x, y, width, height
            if board[row, col] == 1:
                pygame.draw.circle(screen, RED, (int(col*SQUARESIZE+SQUARESIZE/2), int(row*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)  # center, radius
            elif board[row, col] == 2:
                pygame.draw.circle(screen, YELLOW, (int(col*SQUARESIZE+SQUARESIZE/2), int(row*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)  # center, radius
            else:
                pygame.draw.circle(screen, BLACK, (int(col*SQUARESIZE+SQUARESIZE/2), int(row*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)  # center, radius
    pygame.display.update()


board = create_board()
print(board)
game_over = False
turn = 0

pygame.init()
SQUARESIZE = 100  # pixel count
width = COLOUMN*SQUARESIZE
height = (ROW+1)*SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE/2 - 5)
screen = pygame.display.set_mode(size)  # create screen
draw_board(board)  # draw screen
pygame.display.update()  # update screen

myfont = pygame.font.SysFont('monospace', 75)

while not game_over:
    for event in pygame.event.get():
        # for exit game
        if event.type == pygame.QUIT:
            sys.exit()

        # for piece selection
        if event.type == pygame.MOUSEMOTION:
            # surface, color, x, y, width, height
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                # surface, color, center, radius
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
        pygame.display.update()

        # for piece drop
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            print(event.pos)
            # ask for player 1 input
            if turn == 0:
                print('Player 1: ')
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    print(f'debug 1: {row}, {col}')
                    drop_piece(board, row, col, 1)
                    if winning_move(board, 1):
                        label = myfont.render('Player 1 wins', 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True
                else:
                    print('Player 1: not valid move')

            # ask for player 2 input
            else:
                print('Player 2: ')
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    print(f'debug 2: {row}, {col}')
                    drop_piece(board, row, col, 2)
                    if winning_move(board, 2):
                        label = myfont.render('Player 2 wins', 1, YELLOW)
                        screen.blit(label, (40, 10))
                        game_over = True
                else:
                    print('Player 2: not valid move')

            print(board)
            draw_board(board)
            turn += 1
            turn = turn % 2

            if game_over:
                pygame.time.wait(3000)
