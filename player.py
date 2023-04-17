import chess
import chess.polyglot
import copy

POS_INF = 1000000000
NEG_INF = -1000000000

class Player():
    def __init__(self, color): self.color = color

    def getMove(self, board): pass

    def eval(self, board, color):
        
        if board.outcome():
            if board.outcome().winner == color:
                return POS_INF
            elif board.outcome().winner:
                return NEG_INF
            else:
                return 0
        eval = 0
        dsi = 0
        bb = chess.BaseBoard(board.board_fen())
        eval += len(bb.pieces(chess.PAWN, color)) + 3 * len(bb.pieces(chess.BISHOP, color)) + 3 * len(bb.pieces(chess.KNIGHT, color)) + 5 * len(bb.pieces(chess.ROOK, color)) + \
            9 * len(bb.pieces(chess.QUEEN, color)) - (len(bb.pieces(chess.PAWN, not color)) + 3 * len(bb.pieces(chess.BISHOP, not color)) + 3 * len(bb.pieces(chess.KNIGHT, not color)) +\
                 5 * len(bb.pieces(chess.ROOK, not color)) + 9 * len(bb.pieces(chess.QUEEN, not color)))
        

        pawns = bb.pieces(chess.PAWN, color)
        files = chess.BB_FILES
        for file in files:
            if len(pawns.intersection(file)) > 1:
                dsi -= 1
        for pos in pawns:
            if bb.piece_at(pos + 8):
                dsi -= 1
        for pos in pawns:
            if pos % 8 == 0:
                if len(pawns.intersection(files[1])) == 0:
                    dsi -= 1
            elif pos % 8 == 7:
                if len(pawns.intersection(files[6])) == 0:
                    dsi -= 1
            else:
                if len(pawns.intersection(files[pos % 8 - 1])) == 0 and len(pawns.intersection(files[pos % 8 + 1])) == 0:
                    dsi -= 1
        pawns = bb.pieces(chess.PAWN, not color)
        for file in files:
            if len(pawns.intersection(file)) > 1:
                dsi += 1
        for pos in pawns:
            if bb.piece_at(pos - 8):
                dsi += 1
        for pos in pawns: 
            if pos % 8 == 0:
                if len(pawns.intersection(files[1])) == 0:
                    dsi += 1
            elif pos % 8 == 7:
                if len(pawns.intersection(files[6])) == 0:
                    dsi += 1
            else:
                if len(pawns.intersection(files[pos % 8 - 1])) == 0 and len(pawns.intersection(files[pos % 8 + 1])) == 0:
                    dsi += 1
        eval += 0.5 * dsi

        board.push(chess.Move.null())
        if board.turn == color:
            eval += board.legal_moves.count()
            board.push(chess.Move.null())
            eval -= 0.1 * board.legal_moves.count()
        else:
            eval -= board.legal_moves.count()
            eval += 0.1 * board.legal_moves.count()
        board.pop()
        return eval
       
         
class ChessBot(Player):
    def __init__(self, color, depth):
        super(ChessBot, self).__init__(color)
        self.depth = depth

    def getMove(self, board):
        with chess.polyglot.open_reader("baron30.bin") as reader:
            pos = reader.get(board)
            if pos:
                pos = reader.weighted_choice(board)
                return pos.move
            else:
                return self.max_value(board, self.depth, NEG_INF, POS_INF)[1]

    def max_value(self, board, curr_depth, a, b):
        if curr_depth == 0:
            return (self.eval(board, self.color), None)
        util = NEG_INF
        nm = None
        legalMoves = board.legal_moves
        if legalMoves.count() == 0:
            return (self.eval(board, self.color), None)
        for move in legalMoves:
            modified_board = copy.deepcopy(board)
            modified_board.push(move)
            possible_util = self.min_value(modified_board, curr_depth - 1, a, b)[0]
            if util < possible_util:
                util = possible_util
                nm = move
            if util >= b:
                return (util, nm)
            a = max(a, util)
        return (util, nm)

    def min_value(self, board, curr_depth, a, b):
        if curr_depth == 0:
            return (self.eval(board, self.color),None)
        util = POS_INF
        nm = None
        legalMoves = board.legal_moves
        if legalMoves.count() == 0:
            return (self.eval(board, self.color), None)
        for move in legalMoves:
            modified_board = copy.deepcopy(board)
            modified_board.push(move)
            possible_util = self.max_value(modified_board, curr_depth - 1, a, b)[0]
            if util > possible_util:
                util = possible_util
                nm = move
            if util <= a:
                return (util, nm)
            b = min(b, util)
        return (util, nm)

class HumanPlayer(Player):
    def __init__(self, color): super(HumanPlayer, self).__init__(color)
    def getMove(self, board): raise NotImplementedError('Human Player functionality is implemented externally.')

def makePlayer(playerType, color, depth=5):
    player = playerType[0].lower()
    if player == 'p': return HumanPlayer(color)
    elif player == 'b': return ChessBot(color, depth)
    else: raise NotImplementedError('Unrecognized player type {}'.format(playerType))