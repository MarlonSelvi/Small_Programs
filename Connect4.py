import sys
import numpy as np
import pygame
import math

COL_SIZE = 7
ROW_SIZE = 6
BLUE = (0,0,255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255,255,0)


def create_board():
    board = np.zeros((ROW_SIZE, COL_SIZE))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_SIZE - 1][col] == 0


def next_open_row(board, col):
    for r in range(ROW_SIZE):
        if (board[r][col] == 0):
            return r


def printBoard(board):
    print(np.flip(board, axis=0))


def winning_move(board, piece):
    # Checks for Horizontal wins
    for c in range(COL_SIZE - 3):
        for r in range(ROW_SIZE):
            if (board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece
                    and board[r][c + 3] == piece):
                return True
    # Checks for Vertical wins
    for c in range(COL_SIZE):
        for r in range(ROW_SIZE - 3):
            if (board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece
                    and board[r + 3][c] == piece):
                return True

    #Checks for Diagonal (left to right)
    for c in range(COL_SIZE):
        for r in range(ROW_SIZE - 3):
            if (board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece
                    and board[r + 3][c] == piece):
                return True

    #Checks for Diagonal (Top - Right to Bottom - Left)
    for c in range(COL_SIZE - 3):
        for r in range(ROW_SIZE - 3):
            if (board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece
                    and board[r + 3][c + 3] == piece):
                return True
    #Cheks for Diagonal (Bottom-Left to Top-Right)
    for c in range(COL_SIZE - 3):
        for r in range(3, ROW_SIZE):
            if (board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece
                    and board[r - 3][c + 3] == piece):
                return True


def draw_board(board):
    for c in range(COL_SIZE):
        for r in range(ROW_SIZE):
            pygame.draw.rect(screen, BLUE,(c*SQUARESIZE, r*SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK,(int(c*SQUARESIZE + SQUARESIZE/ 2), int(r*SQUARESIZE+SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    for c in range(COL_SIZE):
        for r in range(ROW_SIZE):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED,(int(c*SQUARESIZE + SQUARESIZE/ 2), height - int(r*SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW,(int(c*SQUARESIZE + SQUARESIZE/ 2), height - int(r*SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()


board = create_board()
printBoard(board)
turn = 0
game_over = False

pygame.init()

#Size of one square that includes one socket of the frame
#and the space in the middle for the pieces (Red or Yellow)
SQUARESIZE = 100

width = COL_SIZE * SQUARESIZE
height = (ROW_SIZE + 1) * SQUARESIZE
RADIUS = int(SQUARESIZE/2 - 5)

size = (width, height)
#Can get these funtions from Pygame.org/docs
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont('monospace', 75)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            #Input from Player 1
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))
                if is_valid_location(board, col):
                    row = next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if winning_move(board, 1):
                        label = myfont.render("PLAYER WINS!", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True
            # # Input from Player 2
            else:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))
                if is_valid_location(board, col):
                    row = next_open_row(board, col)
                    drop_piece(board, row, col, 2)

                    if winning_move(board, 2):
                        label = myfont.render("PLAYER WINS!", 1, YELLOW)
                        screen.blit(label, (40, 10))
                        game_over = True

            turn += 1
            turn = turn % 2

            draw_board(board)
            printBoard(board)

            if game_over:
                pygame.time.wait(3500)
