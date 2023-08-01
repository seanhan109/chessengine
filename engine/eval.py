import os.path
import torch
import numpy as np
from neural_net import ChessNet
from chess import Board
import copy
from MCTS import UCT_search
import pickle
import torch.multiprocessing as mp


def save_as_pickle(filename, data):
    completeName = os.path.join("./evaluator_data/",filename)

    with open(completeName, 'wb') as output:
        pickle.dump(data, output)

class arena():
    def __init__(self, current_chessnet, best_chessnet):
        self.current = current_chessnet
        self.best = best_chessnet
    
    def play_round(self):
        if np.random.uniform(0,1) <= 0.5:
            white = self.current
            black = self.best
            w = "current"
            b = "best"
        else:
            black = self.current
            white = self.best
            b = "current"
            w = "best"
            current_board = Board()