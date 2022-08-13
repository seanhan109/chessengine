from ast import AsyncFunctionDef
import chess
import player

if __name__ == '__main__':
    board = chess.Board()

    p1_type = 'p'#input()
    p2_type = 'b'#input()
    depth = int(input())

    p1 = player.makePlayer(p1_type, chess.WHITE, depth)
    p2 = player.makePlayer(p2_type, chess.BLACK, depth)

    if p1.color == p2.color:
        raise Exception('Players must be different colors')
    while not (board.is_checkmate() or board.is_stalemate() or board.is_insufficient_material() or board.is_variant_end()):
        print(board)
        print(' ')
        turn = board.turn
        if turn:
            if p1.color:
                if isinstance(p1, player.HumanPlayer):
                    nm = input()
                    try:
                        board.push_san(nm)
                    except:
                        print('Illegal move. Try again.')
                else:
                    board.push(p1.getMove(board))
            else:
                if isinstance(p2, player.HumanPlayer):
                    nm = input()
                    try:
                        board.push_san(nm)
                    except:
                        print('Illegal move. Try again.')
                else:
                    board.push(p2.getMove(board))
        else:
            if not p1.color:
                if isinstance(p1, player.HumanPlayer):
                    nm = input()
                    try:
                        board.push_san(nm)
                    except:
                        print('Illegal move. Try again.')
                else:
                    nm = p1.getMove(board)
            else:
                if isinstance(p2, player.HumanPlayer):
                    nm = input()
                    try:
                        board.push_san(nm)
                    except:
                        print('Illegal move. Try again.')
                else:
                    board.push(p2.getMove(board))
    print(board)
    print(board.result())