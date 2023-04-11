import math
import random
import numpy as np

Y = 1
R = 2
E = 0
PIECES = [Y, R]


ROW_COUNT = 6
COLUMN_COUNT = 7

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4

def initial_state():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board

def actions(board):
    valid_locations = []
    for col in range(7):
        if not board[5][col]:
            valid_locations.append(col)

    return valid_locations

def result(board, col, piece):
    board[available_row(board, col)][col] = piece
    return board

def available_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r
        
def to_column(board, col):
    return [board[i][col] for i in range(len(board))]
    
def to_row(board, row):
    return board[row]

def winner(board):
 
    for piece in PIECES:
        
        for c in range(4):
            for r in range(6):
                if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                    return piece

        for c in range(7):
            for r in range(3):
                if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                    return piece

        for c in range(4):
            for r in range(3):
                if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                    return piece
    
        for c in range(4):
            for r in range(3, 6):
                if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                    return piece
    return None

def terminal(board):
    if winner(board) or not len(actions(board)):
       return True
    else:
       return False
   
def utility(window, piece):
    score = 0

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(E) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(E) == 2:
        score += 2

    if window.count(Y) == 3 and window.count(E) == 1:
        score -= 4

    return score


def score_position(board, piece):
    score = 0

    center_array = [i for i in to_column(board, COLUMN_COUNT//2)]
    center_count = center_array.count(piece)
    score += center_count * 3

    for r in range(ROW_COUNT):
        row_array = [i for i in to_row(board,r)]
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += utility(window, piece)

    for c in range(COLUMN_COUNT):
        col_array = [i for i in to_column(board,c)]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += utility(window, piece)

    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += utility(window, piece)

    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += utility(window, piece)

    return score


def minimax(board, depth, is_ai):
    valid_locations = actions(board)
    if depth == 0 or terminal(board):
        if terminal(board):
            if winner(board) == AI_PIECE:
                return (None, 10000)
            elif winner(board) == PLAYER_PIECE:
                return (None, -10000)
            else: 
                return (None, 0)
        else: 
            return (None, score_position(board, AI_PIECE))
    if is_ai:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            b_copy = result(board.copy(), col, AI_PIECE)
            new_score = minimax(b_copy, depth-1, False)[1]
            if new_score > value:
                value = new_score
                column = col
        return (column, value)

    else: 
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            b_copy = result(board.copy(), col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth-1, True)[1]
            if new_score < value:
                value = new_score
                column = col
        return (column, value)
    
def main():
    print("RUN CONNECT_FOUR_APP.PY TO PLAY GAME")
    print("RUN CONNECT_FOUR_ARDUINO.PY TO RUN ARDUINO")
    
if __name__ == "__main__":
    main()