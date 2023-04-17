import chess
import chess.polyglot
import copy
from eval import eval


class FindMove():
    def __init__(self, board, max_depth):
        self.max_depth = max_depth
        self.board = board
        self.pv = [None] * max_depth
    
    def alpha_beta(self, a, b, depth)->int:
        if depth == 0:
            return eval(self.board)
        util = float('-inf')
        # Maybe not right to add here
        # Might be issues with pv updates
        if self.pv[depth - 1]:
            self.board.push(self.pv[depth-1])
            score = -self.alpha_beta(-b,-a,depth - 1)
            if score >= b:
                return score
            if score > util:
                util = score
            if score > a:
                a = score
                self.pv[depth - 1] = legal_move
            self.board.pop()
        legal_moves = self.board.legal_moves
        #sort moves in order of most promising
        for legal_move in legal_moves:
            self.board.push(legal_move)
            score = -self.alpha_beta(-b, -a, depth - 1)
            if score >= b:
                return score
            if score > util:
                util = score
            if score > a:
                a = score
                self.pv[depth - 1] = legal_move
            self.board.pop()
        return a
    
    def play_move(self, move)->None:
        self.board.push(move)
