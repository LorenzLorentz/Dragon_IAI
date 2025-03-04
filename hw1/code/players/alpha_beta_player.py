from env.base_env import BaseGame
from other_algo.alpha_beta_search import AlphaBetaSearch
from .base_player import BasePlayer
import numpy as np

class AlphaBetaPlayer(BasePlayer):
    def __init__(self):
        self.policy = AlphaBetaSearch()
        self.As = {}

    def __str__(self):
        return "AlphaBeta Player"

    def play(self, state):
        s = state.to_string()
        if s not in self.As:
            self.As[s] = self.policy.get_best_move(state)
        return self.As[s]