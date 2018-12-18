''' minion.py '''
import random

from algorithms import switching_solver
from predictions import make_prediction_fast
from util import find_all_player_indices
from const import logger
import const

from ..village import Player
from .wolf_variants import get_wolf_statements_random, get_statement_expectimax, get_wolf_statements

class Minion(Player):
    ''' Minion Player class. '''

    def __init__(self, player_index, game_roles, original_roles=None):
        # Roles default to None when another player becomes a Minion and realizes it
        super().__init__(player_index)
        self.role = 'Minion'
        self.wolf_indices = self.minion_init(original_roles)

    @staticmethod
    def minion_init(original_roles):
        ''' Initializes Minion - gets Wolf indices. '''
        wolf_indices = []
        if original_roles is not None:
            wolf_indices = set(find_all_player_indices(original_roles, 'Wolf'))
            logger.debug('[Hidden] Wolves are at indices: %s', str(wolf_indices))
        return wolf_indices

    def get_statement(self, stated_roles=None, previous=None):
        ''' Get Minion Statement. '''
        if const.USE_REG_WOLF:
            self.statements = get_wolf_statements(self, stated_roles, previous)
        else:
            self.statements = get_wolf_statements_random(self)

        if const.USE_EXPECTIMAX_WOLF:
            return get_statement_expectimax(self, previous)
        return super().get_statement()

    def eval_fn(self, statement_list):
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
