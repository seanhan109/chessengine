from ast import AsyncFunctionDef
import chess
import player

if __name__ == '__main__':
    board = chess.Board()
    p1_type = input()
    p1_color = input()
    p2_type = input()
    p2_color = input()
    depth = int(input())
    p1 = player.makePlayer(p1_type, p1_color, depth)
    p2 = player.makePlayer(p2_type, p2_color, depth)
    if p1.color == p2.color:
        raise Exception('Players must be different colors')
    while not board.is_checkmate():
        print(board)
        turn = board.turn
        if turn:
            if p1.color == 'w':
                if isinstance(p1, player.HumanPlayer):
                    nm = input()
                    board.push_san(nm)
                else:
                    board.push(p1.getMove(board))
            else:
                if isinstance(p2, player.HumanPlayer):
                    nm = input()
                    board.push_san(nm)
                else:
                    board.push(p2.getMove(board))
        else:
            if p1.color == 'b':
                if isinstance(p1, player.HumanPlayer):
                    nm = input()
                    board.push_san(nm)
                else:
                    nm = p1.getMove(board)
            else:
                if isinstance(p2, player.HumanPlayer):
                    nm = input()
                    board.push_san(nm)
                else:
                    board.push(p2.getMove(board))