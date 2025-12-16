import math
from .board import Board
from .constants import PLAYER_1_BEIGE, PLAYER_2_BLACK, ROWS, COLS
from .piece import Piece


class node:
    def __init__(self, board):
        self.board = board
        self.value = 0
    
    def get_board(self):
        return self.board
    
    def set_value(self, value):
        self.value = value
    
    def get_children(self, maximizing_player, mandatory_jumping):

        children = []
        player_color = PLAYER_1_BEIGE if maximizing_player else PLAYER_2_BLACK

        pieces = self._get_all_pieces(player_color)
        
        all_moves = []
        jump_moves = []
        
        for piece in pieces:
            moves = self.board.get_valid_moves(piece)
            for move_pos, skipped in moves.items():  
                if skipped:  # This is a jump move
                    jump_moves.append((piece, move_pos, skipped))
                else:
                    all_moves.append((piece, move_pos, skipped))
        
        if mandatory_jumping and jump_moves:
            moves_to_consider = jump_moves
        else:
            moves_to_consider = jump_moves + all_moves
        
        for piece, move_pos, skipped in moves_to_consider:
            new_board = self._make_move(self.board, piece, move_pos, skipped)
            child_node = node(new_board)
            children.append(child_node)
        
        return children
    
    def _get_all_pieces(self, color):

        pieces = []
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board.get_piece(row, col)
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces
    
    def _make_move(self, board, piece, move_pos, skipped):
        new_board = self._deepcopy_board(board)
        row, col = move_pos
        
        new_piece = new_board.get_piece(piece.row, piece.col)
        
        new_board.move(new_piece, row, col)
        
        if skipped:
            new_board.remove(skipped)
        
        return new_board
    
    def _deepcopy_board(self, board):
        new_board = Board()
        new_board.board = []
        new_board.beige_left = board.beige_left
        new_board.black_left = board.black_left
        new_board.beige_kings = board.beige_kings
        new_board.black_kings = board.black_kings
        
        for row in range(ROWS):
            new_board.board.append([])
            for col in range(COLS):
                piece = board.get_piece(row, col)
                if piece == 0:
                    new_board.board[row].append(0)
                else:
                    new_piece = Piece(piece.row, piece.col, piece.color)
                    if piece.king:
                        new_piece.make_king()
                    new_board.board[row].append(new_piece)
        
        return new_board


class Checkers:
    @staticmethod
    def minimax(board, depth, alpha, beta, maximizing_player, mandatory_jumping):
        if depth == 0:
            return Checkers.calculate_heuristics(board)
        
        temp_node = node(board)
        current_state = node(temp_node._deepcopy_board(board))
        if maximizing_player is True:
            max_eval = -math.inf
            for child in current_state.get_children(True, mandatory_jumping):
                ev = Checkers.minimax(child.get_board(), depth - 1, alpha, beta, False, mandatory_jumping)
                max_eval = max(max_eval, ev)
                alpha = max(alpha, ev)
                if beta <= alpha:
                    break
            current_state.set_value(max_eval)
            return max_eval
        else:
            min_eval = math.inf
            for child in current_state.get_children(False, mandatory_jumping):
                ev = Checkers.minimax(child.get_board(), depth - 1, alpha, beta, True, mandatory_jumping)
                min_eval = min(min_eval, ev)
                beta = min(beta, ev)
                if beta <= alpha:
                    break
            current_state.set_value(min_eval)
            return min_eval

    @staticmethod
    def get_best_move(board, depth, mandatory_jumping, maximizing_player=True):
        temp_node = node(board)
        current_state = node(temp_node._deepcopy_board(board))

        best_board = None
        if maximizing_player:
            best_eval = -math.inf
            for child in current_state.get_children(True, mandatory_jumping):
                eval_score = Checkers.minimax(child.get_board(), depth - 1, -math.inf, math.inf, False, mandatory_jumping)
                if eval_score > best_eval:
                    best_eval = eval_score
                    best_board = child.get_board()
        else:
            best_eval = math.inf
            for child in current_state.get_children(False, mandatory_jumping):
                eval_score = Checkers.minimax(child.get_board(), depth - 1, -math.inf, math.inf, True, mandatory_jumping)
                if eval_score < best_eval:
                    best_eval = eval_score
                    best_board = child.get_board()

        return best_board
    
    @staticmethod
    def calculate_heuristics(board):
        beige_pieces = 0
        black_pieces = 0
        beige_kings = 0
        black_kings = 0
        
        for row in range(ROWS):
            for col in range(COLS):
                piece = board.get_piece(row, col)
                if piece != 0:
                    if piece.color == PLAYER_1_BEIGE:
                        beige_pieces += 1
                        if piece.king:
                            beige_kings += 1
                    elif piece.color == PLAYER_2_BLACK:
                        black_pieces += 1
                        if piece.king:
                            black_kings += 1
        heuristic = (beige_pieces + beige_kings * 1.5) - (black_pieces + black_kings * 1.5)
        
        if board.winner() == PLAYER_1_BEIGE:
            return 1  
        elif board.winner() == PLAYER_2_BLACK:
            return -1  
        
        return heuristic

def play(self):
    running = True
    ansi_red   = "\033[31m"
    ansi_green = "\033[32m"
    ansi_cyan  = "\033[36m"
    ansi_reset = "\033[0m"
    while running:
        self.print_matrix()
        # Check winner from board directly
        winner = self.board.winner()
        if winner is not None:
            if winner == PLAYER_1_BEIGE:
                print(ansi_green + "\nYOU WIN!" + ansi_reset)
            else:
                print(ansi_red + "\nYOU LOSE!" + ansi_reset)
            break

        if self.player_turn:
            print(ansi_cyan + "\nPlayer's turn." + ansi_reset)
            self.get_player_input()
        else:
            print(ansi_cyan + "\nComputer's turn." + ansi_reset)
            print("Thinking...")
            
            new_board = Checkers.get_best_move(
                self.board,
                depth=4,
                mandatory_jumping=self.mandatory_jumping,
                maximizing_player=False
            )
            if new_board:
                self.board = new_board
            else:
                print(ansi_green + "Computer has no moves. YOU WIN!" + ansi_reset)
                break

        # Optional surrender logic
        diff = self.board.black_left - self.board.beige_left
        if diff >= 7 and self.player_turn:
            wish = input("You are far behind. Do you want to surrender? (yes/no): ")
            if wish.lower() in ["", "yes", "y"]:
                print(ansi_cyan + "Game surrendered." + ansi_reset)
                break

        self.player_turn = not self.player_turn
