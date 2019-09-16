''' minion.py '''
from typing import List
import random

from src.statements import Statement
from src.algorithms import switching_solver
from src.predictions import make_prediction_fast
from src.const import logger
from src import const, util

from ..village import Player
from .wolf_variants import get_wolf_statements_random, get_statement_expectimax, get_wolf_statements

class Minion(Player):
    ''' Minion Player class. '''

    def __init__(self, player_index: int, game_roles: List[str], original_roles: List[str]):
        # Roles default to [] when another player becomes a Minion and realizes it
        super().__init__(player_index)
        self.wolf_indices = self.minion_init(original_roles)

    def minion_init(self, original_roles: List[str]) -> List[int]:
        ''' Initializes Minion - gets Wolf indices. '''
        wolf_indices = []
        if original_roles:
            wolf_indices = util.find_all_player_indices(original_roles, 'Wolf')
            logger.debug(f'[Hidden] Wolves are at indices: {wolf_indices}')
            if self.is_user: logger.info(f'Wolves are at indices: {wolf_indices}')

        return wolf_indices

    def get_statement(self, stated_roles: List[str], previous: List[Statement]) -> Statement:
        ''' Get Minion Statement. '''
        if const.USE_REG_WOLF:
            self.statements += get_wolf_statements(self, stated_roles, previous)
        else:
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
        for wolfi in self.wolf_indices:
            if predictions[wolfi] == 'Wolf':
                val -= 5
            if 'Wolf' in solver_result.possible_roles[wolfi]:
                val -= 5
        return val
