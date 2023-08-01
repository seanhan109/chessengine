import pickle
import os
import collections
import numpy as np
import math
from chess import board
import copy
import torch
import torch.multiprocessing as mp
from neural_net import ChessNet
import datetime

class UCTNode():
    def __init__(self, game, move, parent=None):
        self.game = game
        self.move = move
        self.is_expanded = False
        self.parent = parent
        self.children = {}
        self.child_priors = np.zeros([4672],dtype=np.float32)
        self.child_total_value = np.zeros([4672], dtype=np.float32)
        self.child_number_visits = np.zeros([4672], dtype=np.float32)
        self.action_indices = []

    @property
    def num_visits(self):
        return self.parent.child_number_visits[self.move]
    
    @num_visits.setter
    def num_visits(self, value):
        self.parent.child_number_visits[self.move] = value

    @property
    def tot_value(self):
        return self.parent.child_total_value[self.move]
    
    @tot_value.setter
    def tot_value(self, value):
        self.parent.child_total_value[self.move] = value

    def child_Q(self):
        return self.child_total_value / (1 + self.child_number_visits)
    
    def child_U(self):
        return math.sqrt(self.num_visits) * (abs(self.child_priors) / (1 + self.child_number_visits))
    
    def best_child(self):
        if self.action_indices != []:
            bestmove = self.child_Q() + self.child_U()
            bestmove = self.action_indices[np.argmax(bestmove[self.action_indices])]
        else:
            bestmove = np.argmax(self.child_Q() + self.child_U())
        return bestmove
    
    def select_leaf(self):
        current = self
        while current.is_expanded:
            best_move = current.best_child()
            current = current.maybe_add_child(best_move)
        return current
    
    def add_dirichlet_noise(self, action_indices,child_priors):
        valid_child_priors = child_priors[action_indices]
        valid_child_priors = 0.75 * valid_child_priors + 0.25 * np.random.dirichlet(np.zeros([len(valid_child_priors)], dtype=np.float32) + 0.3)
        child_priors[action_indices] = valid_child_priors
        return child_priors
    
    def expand(self, child_priors):
        self.is_expanded = True
        action_indices = []
        c_p = child_priors
        for action in self.game.legal_moves:
            if 

if __name__ =="__main__":
    net_to_play = "current_net_trained8_iter1.pth.tar"
    mp.set_start_method("spawn",force=True)
    net = ChessNet()
    cuda = torch.cuda.is_available()
    if cuda:
        net.cuda()
    net.share_memory()
    net.eval()
    