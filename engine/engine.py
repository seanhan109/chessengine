import chess
from search import FindMove

### for now, only supports white
def Engine():
    def __init__(self, color, depth):
        self.color = color
        self.move_finder = FindMove(chess.Board(), depth)