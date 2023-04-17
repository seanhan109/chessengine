import chess
import chess.polyglot
import copy
from eval import eval


class FindMove():
    def __init__(self, board, max_depth):
        self.depth = max_depth
        self.board = board
        self.trans_table = {}
    
    def alpha_beta(self, a, b, depth)->int:
        if depth == 0:
            return self.quiescence(a, b)
        legal_moves = self.board.legal_moves
        #sort moves in order of most promising
        for legal_move in legal_moves:
            self.board.push(legal_move)
            score = -self.alpha_beta(-b, -a, depth - 1)
            self.board.pop()
            if score >= b:
                return score
            if score > a:
                a = score
        return a
    
    def quiescence(self, a, b)->int:
        stand_pat = eval(self.board)
        if (stand_pat >= b):
            return b
        if (stand_pat > a):
            a = stand_pat
        legal_moves = self.board.legal_moves
        for legal_move in legal_moves:
            if not self.board.is_capture(legal_move):
                continue
            self.board.push(legal_move)
            score = -self.quiescence(-b, -a)
            self.board.pop()

            if score >= b:
                return b
            if score > a:
                a = score
        return a
