''' tanner.py '''
from typing import Dict, List
import random

from src.statements import Statement
from src.algorithms import switching_solver
from src.predictions import make_prediction_fast
from src import const

from ..village import Player
from .wolf_variants import get_wolf_statements_random, get_statement_expectimax

class Tanner(Player):
    ''' Tanner Player class. '''

    def __init__(self, player_index: int):
        # Roles default to [] when another player becomes a Tanner and realizes it
        super().__init__(player_index)

    @classmethod
    def awake_init(cls, player_index: int, game_roles: List[str], original_roles: List[str]):
        ''' Initializes Tanner when night falls. '''
        return cls(player_index)

    def get_statement(self, stated_roles: List[str], previous: List[Statement]) -> Statement:
        ''' Get Tanner Statement. '''
        self.statements += get_wolf_statements_random(self)

        if const.USE_EXPECTIMAX_WOLF:
            return get_statement_expectimax(self, previous)
        return super().get_statement(stated_roles, previous)

    def eval_fn(self, statement_list: List[Statement]) -> int:
        '''
        Evaluates a complete or incomplete game.
        # wolves in a positions - # of ones that are actually wolves, size of set
        '''
        solver_result = random.choice(switching_solver(statement_list))
        predictions = make_prediction_fast(solver_result)
        val = 10
        if not predictions:
            return -10
        if predictions[self.player_index] == 'Wolf':
            val += 10
        return val

    def json_repr(self) -> Dict:
        ''' Gets JSON representation of a Tanner player. '''
        return {'type': self.role, 'player_index': self.player_index}
