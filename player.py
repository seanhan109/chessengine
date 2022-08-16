import chess
import chess.polyglot
import copy

POS_INF = 1000000000
NEG_INF = -1000000000
piece_values = {'p':1, 'n':3, 'b':3, 'r':5, 'q':9,'k':0,'P':1,'N':3, 'B':3,'R':5,'Q':9,'K':0}
center_pos = [chess.D4, chess.D5, chess.E5, chess.E4]
#chess.D4, chess.D5, chess.E4, chess.E5 are very important squares

class Player():
    def __init__(self, color): self.color = color

    def getMove(self, board): pass

    def eval(self, board, color):
        eval = 0
        lob = chess.SQUARES
        for pos in lob:
            piece = board.piece_at(pos)
            if piece:
                if piece.color:
                    if color:
                        eval += piece_values[piece.symbol()]
                    else:
                        eval -= piece_values[piece.symbol()]
                else:
                    if not color:
                        eval += piece_values[piece.symbol()]
                    else:
                        eval -= piece_values[piece.symbol()]
        return eval
                
        # modified_board = copy.deepcopy(board)
        # modified_board.push(chess.Move.null())
        # if board.fullmove_number > 10:
        #     eval = -modified_board.legal_moves.count()
        # else:
        #     eval = 0
        # modified_board.pop()
        # lob = chess.SQUARES
        # for pos in lob:
        #     piece = board.piece_at(pos)
        #     if piece:
        #         #-1 for the person in turn
        #         attack_eq = len(list(board.attackers(color, pos))) - len(list(board.attackers(not color, pos))) + (1 if color else -1)
        #         if piece.color:
        #             if color:
        #                 if pos in center_pos and piece.symbol == 'P':
        #                     eval += 2
        #                 eval += piece_values[piece.symbol()]
        #                 eval += 0.1 * piece_values[piece.symbol()] * attack_eq
        #             else:
        #                 if pos in center_pos and piece.symbol == 'p':
        #                     eval -= 2
        #                 eval -= piece_values[piece.symbol()]
        #                 eval -= 0.1 * piece_values[piece.symbol()] * attack_eq
        #         else:
        #             if not color:
        #                 if pos in center_pos and piece.symbol == 'p':
        #                     eval += 2
        #                 eval += piece_values[piece.symbol()]
        #                 eval += 0.1 * piece_values[piece.symbol()] * attack_eq
        #             else:
        #                 if pos in center_pos and piece.symbol == 'P':
        #                     eval -= 2
        #                 eval -= piece_values[piece.symbol()]
        #                 eval -= 0.1 * piece_values[piece.symbol()] * attack_eq

        # return eval

class ChessBot(Player):
    def __init__(self, color, depth):
        super(ChessBot, self).__init__(color)
        self.depth = depth

    def getMove(self, board):
        with chess.polyglot.open_reader("Balsa_v110221.pgn") as reader:

            try:
                pos = reader.weighted_choice(board)
                return pos.move
            except:
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