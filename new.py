import numpy as np

ROW_COUNT = 6
COLUMN_COUNT = 7

def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT), dtype=int)

def is_valid_move(board, col):
    return board[ROW_COUNT - 1][col] == 0

def drop_piece(board, col, player):
    for row in range(ROW_COUNT):
        if board[row][col] == 0:
            board[row][col] = player
            break

def winning_move(board, player):
    # Check for a horizontal win
    for row in range(ROW_COUNT):
        for col in range(COLUMN_COUNT - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True

    # Check for a vertical win
    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True

    # Check for a diagonal win (positive slope)
    for row in range(ROW_COUNT - 3):
        for col in range(COLUMN_COUNT - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True

    # Check for a diagonal win (negative slope)
    for row in range(3, ROW_COUNT):
        for col in range(COLUMN_COUNT - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True

    return False

def evaluate_board(board):
    player1 = 1
    player2 = 2

    if winning_move(board, player1):
        return -1

    elif winning_move(board, player2):
        return 1

    else:
        return 0

def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or winning_move(board, 1) or winning_move(board, 2):
        return evaluate_board(board)

    if maximizing_player:
        max_eval = float('-inf')
        for col in range(COLUMN_COUNT):
            if is_valid_move(board, col):
                temp_board = board.copy()
                drop_piece(temp_board, col, 2)
                eval = minimax(temp_board, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return max_eval
    else:
        min_eval = float('inf')
        for col in range(COLUMN_COUNT):
            if is_valid_move(board, col):
                temp_board = board.copy()
                drop_piece(temp_board, col, 1)
                eval = minimax(temp_board, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return min_eval

import random

def best_move(board):
    best_score = float('-inf')
    best_moves = []
    for col in range(COLUMN_COUNT):
        if is_valid_move(board, col):
            temp_board = board.copy()
            drop_piece(temp_board, col, 2)
            score = minimax(temp_board, 7, float('-inf'), float('inf'), False)  # Adjust depth as needed
            if score > best_score:
                best_score = score
                best_moves = [col]
            elif score == best_score:
                best_moves.append(col)
    return random.choice(best_moves)

if __name__ == "__main__":
    board = create_board()
    game_over = False
    current_player = 1
 
    while not game_over:
        if current_player == 1:
            col = int(input(f"Player 1, enter column (0-{COLUMN_COUNT - 1}): "))
        else:
            col = best_move(board)
        if is_valid_move(board, col):
            drop_piece(board, col, current_player)
            print(np.flip(board, 0))
            if winning_move(board, current_player):
                print(f"Player {current_player} wins!")
                game_over = True
            current_player = 3 - current_player  # Switch players