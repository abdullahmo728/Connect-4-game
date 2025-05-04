import math
import random

# Constants for the game
ROWS = 6
COLS = 7
PLAYER = 1
AI = 2
EMPTY = 0

class Connect4GameLogic:
    def __init__(self, k=4, use_alpha_beta=True):
        self.board = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]  
        self.current_player = PLAYER  
        self.k = k  
        self.use_alpha_beta = use_alpha_beta  

    def reset_game(self):
        self.board = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
        self.current_player = PLAYER

    def make_move(self, col, player):
        """Make a move and return True if player wins."""
        for row in range(ROWS - 1, -1, -1):
            if self.board[row][col] == EMPTY:
                self.board[row][col] = player
                return self.check_winner(player)
        return False

    def is_valid_move(self, col):
        return self.board[0][col] == EMPTY

    def is_board_full(self):
        return all(self.board[0][col] != EMPTY for col in range(COLS))

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        valid_locations = [col for col in range(COLS) if board[0][col] == EMPTY]
        is_terminal = self.is_terminal_node(board)

        if depth == 0 or is_terminal:
            if is_terminal:
                if self.check_winner_on_board(board, AI):
                    return (math.inf, None)
                elif self.check_winner_on_board(board, PLAYER):
                    return (-math.inf, None)
                else:
                    return (0, None)
            else:
                return (self.heuristic_evaluation(board), None)

        if maximizing_player:
            value = -math.inf
            best_col = random.choice(valid_locations)
            for col in valid_locations:
                temp_board = [row[:] for row in board]
                self.make_temp_move(temp_board, col, AI)
                new_score, _ = self.minimax(temp_board, depth-1, alpha, beta, False)
                if new_score > value:
                    value = new_score
                    best_col = col
                alpha = max(alpha, value)
                if self.use_alpha_beta and alpha >= beta:
                    break
            return value, best_col

        else:
            value = math.inf
            best_col = random.choice(valid_locations)
            for col in valid_locations:
                temp_board = [row[:] for row in board]
                self.make_temp_move(temp_board, col, PLAYER)
                new_score, _ = self.minimax(temp_board, depth-1, alpha, beta, True)
                if new_score < value:
                    value = new_score
                    best_col = col
                beta = min(beta, value)
                if self.use_alpha_beta and alpha >= beta:
                    break
            return value, best_col

    def make_temp_move(self, board, col, player):
        for row in range(ROWS - 1, -1, -1):
            if board[row][col] == EMPTY:
                board[row][col] = player
                return True
        return False

    def heuristic_evaluation(self, board):
        score = 0
        center_array = [board[row][COLS // 2] for row in range(ROWS)]
        score += center_array.count(AI) * 3

        for row in range(ROWS):
            row_array = [board[row][col] for col in range(COLS)]
            for col in range(COLS - 3):
                window = row_array[col:col + 4]
                score += self.evaluate_window(window)

        for col in range(COLS):
            col_array = [board[row][col] for row in range(ROWS)]
            for row in range(ROWS - 3):
                window = col_array[row:row + 4]
                score += self.evaluate_window(window)

        for row in range(ROWS - 3):
            for col in range(COLS - 3):
                window = [board[row+i][col+i] for i in range(4)]
                score += self.evaluate_window(window)

        for row in range(3, ROWS):
            for col in range(COLS - 3):
                window = [board[row-i][col+i] for i in range(4)]
                score += self.evaluate_window(window)

        return score

    def evaluate_window(self, window):
        score = 0
        if window.count(AI) == 4:
            score += 100
        elif window.count(AI) == 3 and window.count(EMPTY) == 1:
            score += 5
        elif window.count(AI) == 2 and window.count(EMPTY) == 2:
            score += 2
        if window.count(PLAYER) == 3 and window.count(EMPTY) == 1:
            score -= 4
        return score

    def check_winner(self, player):
        for row in range(ROWS):
            for col in range(COLS - 3):
                if all(self.board[row][col + i] == player for i in range(4)):
                    return True
        for col in range(COLS):
            for row in range(ROWS - 3):
                if all(self.board[row + i][col] == player for i in range(4)):
                    return True
        for row in range(ROWS - 3):
            for col in range(COLS - 3):
                if all(self.board[row + i][col + i] == player for i in range(4)):
                    return True
        for row in range(3, ROWS):
            for col in range(COLS - 3):
                if all(self.board[row - i][col + i] == player for i in range(4)):
                    return True
        return False

    def check_winner_on_board(self, board, player):
        for row in range(ROWS):
            for col in range(COLS - 3):
                if all(board[row][col + i] == player for i in range(4)):
                    return True
        for col in range(COLS):
            for row in range(ROWS - 3):
                if all(board[row + i][col] == player for i in range(4)):
                    return True
        for row in range(ROWS - 3):
            for col in range(COLS - 3):
                if all(board[row + i][col + i] == player for i in range(4)):
                    return True
        for row in range(3, ROWS):
            for col in range(COLS - 3):
                if all(board[row - i][col + i] == player for i in range(4)):
                    return True
        return False

    def is_terminal_node(self, board):
        return self.check_winner_on_board(board, PLAYER) or self.check_winner_on_board(board, AI) or self.is_board_full()
