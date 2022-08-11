from chess import Board, Move, STARTING_FEN
import copy

POS_INF = 1000000000
NEG_INF = -1000000000

class Player():
    def __init__(self, color): self.color = color

    def getMove(self, board): pass

    def eval(self, board, symbol):
        return board.legal_moves.count()

class ChessBot(Player):
    def __init__(self, color, depth):
        super(ChessBot, self).__init__(color)
        self.depth = depth

    def getMove(self, board):
        return self.max_value(board, self.depth, NEG_INF, POS_INF)[1]

    def max_value(self, board, curr_depth, a, b):
        if curr_depth == 0:
            return [self.eval(board, self.color), None]
        util = NEG_INF
        nm = None
        legalMoves = board.legal_moves
        if legalMoves.count() == 0:
            return [self.eval(board, self.color), None]
        for move in legalMoves:
            modified_board = copy.deepcopy(board)
            modified_board.push(move)
            possible_util = self.min_value(modified_board, curr_depth - 1, a, b)[0]
            if util < possible_util:
                util = possible_util
                nm = move
            if util >= b:
                return [util, nm]
            a = max(a, util)
        return [util, nm]

    def min_value(self, board, curr_depth, a, b):
        if curr_depth == 0:
            return [self.eval(board, self.color),None]
        util = POS_INF
        nm = None
        legalMoves = board.legal_moves
        if legalMoves.count() == 0:
            return [self.eval(board, self.color), None]
        for move in legalMoves:
            modified_board = copy.deepcopy(board)
            modified_board.push(move)
            possible_util = self.max_value(modified_board, curr_depth - 1, a, b)[0]
            if util > possible_util:
                util = possible_util
                nm = move
            if util <= a:
                return [util, nm]
            b = min(b, util)
        return [util, nm]

class HumanPlayer(Player):
    def __init__(self, color): super(HumanPlayer, self).__init__(color)
    def getMove(self, board): raise NotImplementedError('Human Player functionality is implemented externally.')

def makePlayer(playerType, color, depth=5):
    player = playerType[0].lower()
    if player == 'p': return HumanPlayer(color)
    elif player == 'b': return ChessBot(color, depth)
    else: raise NotImplementedError('Unrecognized player type {}'.format(playerType))