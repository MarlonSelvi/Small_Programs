import random
import sys
import numpy as np
import pygame
import math

COL_SIZE = 7
ROW_SIZE = 6
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2
WINDOW_LENGHT = 4


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

    # Checks for Diagonal (left to right)
    for c in range(COL_SIZE):
        for r in range(ROW_SIZE - 3):
            if (board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece
                    and board[r + 3][c] == piece):
                return True

    # Checks for Diagonal (Top - Right to Bottom - Left)
    for c in range(COL_SIZE - 3):
        for r in range(ROW_SIZE - 3):
            if (board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece
                    and board[r + 3][c + 3] == piece):
                return True
    # Cheks for Diagonal (Bottom-Left to Top-Right)
    for c in range(COL_SIZE - 3):
        for r in range(3, ROW_SIZE):
            if (board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece
                    and board[r - 3][c + 3] == piece):
                return True


def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2
    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score


def score_position(board, piece):
    score = 0

    #Score for Center Column
    center_array = [int(i) for i in list(board[:, COL_SIZE // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Horizontal Score
    for r in range(ROW_SIZE):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COL_SIZE - 3):
            window = row_array[c:c + WINDOW_LENGHT]
            score += evaluate_window(window, piece)

    # Vertical Score
    for c in range(COL_SIZE):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_SIZE - 3):
            window = col_array[r:r + WINDOW_LENGHT]
            score += evaluate_window(window, piece)

    # Positive Slope Score
    for r in range(ROW_SIZE - 3):
        for c in range(COL_SIZE - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGHT)]
            score += evaluate_window(window, piece)

    # Negative Slope Score
    for r in range(ROW_SIZE - 3):
        for c in range(COL_SIZE - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGHT)]
            score += evaluate_window(window, piece)

    return score


def get_valid_locations(board):
    valid_locations = []
    for c in range(COL_SIZE):
        if is_valid_location(board, c):
            valid_locations.append(c)
    return valid_locations

def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, isMaximizing):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 1000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -1000000000)
            else:#Nothing more can be done
                return (None, 0)
        else:
            return (None, score_position(board, AI_PIECE))

    if isMaximizing:
        val = -math.inf
        best_col = random.choice(valid_locations)
        for c in valid_locations:
            row = next_open_row(board, c)
            b_copy = board.copy()
            drop_piece(b_copy, row, c, AI_PIECE)
            new_val = minimax(b_copy, depth - 1,alpha, beta, False)[1]
            if new_val > val:
                val = new_val
                best_col = c
            alpha = max(alpha, val)
            if alpha >= beta:
                break
        return best_col, val
    else:
        val = math.inf
        best_col = random.choice(valid_locations)
        for c in valid_locations:
            row = next_open_row(board, c)
            b_copy = board.copy()
            drop_piece(b_copy, row, c, PLAYER_PIECE)
            new_val = minimax(b_copy, depth - 1,alpha, beta, True)[1]
            if new_val < val:
                val = new_val
                best_col = c
            beta = min(beta, new_val)
            if alpha >= beta:
                break
        return best_col, val


def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = -1000
    best_col = random.choice(valid_locations)
    for c in valid_locations:
        row = next_open_row(board, c)
        temp_board = board.copy()
        drop_piece(temp_board, row, c, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = c

    return best_col


def draw_board(board):
    for c in range(COL_SIZE):
        for r in range(ROW_SIZE):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (
            int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    for c in range(COL_SIZE):
        for r in range(ROW_SIZE):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, YELLOW, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()


board = create_board()
printBoard(board)
game_over = False

pygame.init()

# Size of one square that includes one socket of the frame
# and the space in the middle for the pieces (Red or Yellow)
SQUARESIZE = 100

width = COL_SIZE * SQUARESIZE
height = (ROW_SIZE + 1) * SQUARESIZE
RADIUS = int(SQUARESIZE / 2 - 5)

size = (width, height)
# Can get these funtions from Pygame.org/docs
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont('monospace', 75)

turn = random.randint(PLAYER, AI)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
            pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            # Input from Player 1
            if turn == PLAYER:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))
                if is_valid_location(board, col):
                    row = next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)

                    if winning_move(board, PLAYER_PIECE):
                        label = myfont.render("PLAYER WINS!", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True

                    draw_board(board)
                    printBoard(board)

                    turn += 1
                    turn = turn % 2
            # # Input from Player 2
    if turn == AI and not game_over:
        # col = random.randint(0, COL_SIZE-1)
        #col = pick_best_move(board, AI_PIECE)
        col, minimax_score = minimax(board, 6, -math.inf, math.inf, True)
        if is_valid_location(board, col):
            row = next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)

            if winning_move(board, AI_PIECE):
                label = myfont.render("AI WINS!", 1, YELLOW)
                screen.blit(label, (40, 10))
                game_over = True

            turn += 1
            turn = turn % 2

            draw_board(board)
            printBoard(board)

            if game_over:
                pygame.time.wait(3000)
