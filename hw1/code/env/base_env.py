from typing import List, Tuple
import numpy as np

WHITE, BLACK, EMPTY = -1, 1, 0

EPS = 1e-7

NOTEND = 0

DRAW = EPS

MAX_N = 21

class BaseGame:
    def __init__(self, n:int, m:int) -> None:
        self.n = n
        self.m = m
        self.board = None
        self._action_size = -1
        self._current_player = BLACK
        self._ended = False
    
    def _check_reset(self):
        assert not self._ended, "The game has ended! reset before doing anything."
        assert self.board is not None, "You should reset the game first!"
    
    def _copy_basic_info(self, game:'BaseGame'):
        self.n = game.n
        self.m = game.m
        self._action_size = game._action_size
        self._current_player = game._current_player
        self._ended = game._ended
    
    @property
    def current_player(self):
        return self._current_player
    
    @property
    def observation_size(self):
        return self.n, self.n
    
    @property
    def action_space_size(self):
        return self._action_size
    
    @property
    def action_mask(self):
        raise NotImplementedError
    
    @property
    def observation(self):
        return self.board
    
    @property
    def action_mask(self):
        raise NotImplementedError
    
    @property
    def ended(self):
        return self._ended
    
    def fork(self) -> 'BaseGame':
        raise NotImplementedError
        
    def reset(self) -> np.ndarray:
        self._ended = False
        return None
    
    def step(self, action:int ) -> Tuple[np.ndarray, float, bool]:
        raise NotImplementedError
    
    def get_symmetries(self, policy:np.ndarray) -> List[Tuple[np.ndarray, np.ndarray]]:
        raise NotImplementedError
    
    def get_canonical_form_obs(self) ->np.ndarray:
        raise NotImplementedError
    
    def to_string(self) -> str:
        return NotImplementedError