import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None

def initial_state():
    return [[EMPTY] * 3 for _ in range(3)]

def player(board):
    flat_board = sum(board, [])
    return O if flat_board.count(X) > flat_board.count(O) else X

def actions(board):
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY}

def result(board, action):
    if board[action[0]][action[1]] != EMPTY:
        raise ValueError("Invalid move")
    new_board = deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board

def winner(board):
    lines = board + [list(col) for col in zip(*board)] + [[board[i][i] for i in range(3)], [board[i][2-i] for i in range(3)]]
    for line in lines:
        if line[0] is not None and all(cell == line[0] for cell in line):
            return line[0]
    return None

def terminal(board):
    return winner(board) is not None or all(cell is not EMPTY for row in board for cell in row)

def utility(board):
    win = winner(board)
    return 1 if win == X else -1 if win == O else 0

def minimax(board):
    def max_value(board, alpha, beta):
        if terminal(board):
            return utility(board), None
        v, best_action = float("-inf"), None
        for action in actions(board):
            min_val = min_value(result(board, action), alpha, beta)[0]
            if min_val > v:
                v, best_action = min_val, action
            alpha = max(alpha, v)
            if alpha >= beta:
                break
        return v, best_action

    def min_value(board, alpha, beta):
        if terminal(board):
            return utility(board), None
        v, best_action = float("inf"), None
        for action in actions(board):
            max_val = max_value(result(board, action), alpha, beta)[0]
            if max_val < v:
                v, best_action = max_val, action
            beta = min(beta, v)
            if alpha >= beta:
                break
        return v, best_action

    current_player = player(board)
    return max_value(board, float("-inf"), float("inf"))[1] if current_player == X else min_value(board, float("-inf"), float("inf"))[1]
