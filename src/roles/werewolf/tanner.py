''' tanner.py '''
import random

from algorithms import switching_solver
from predictions import make_prediction_fast
from const import logger
import const

from ..village import Player

class Tanner(Player):
    ''' Tanner Player class. '''

    def __init__(self, player_index, game_roles, ORIGINAL_ROLES=None):
        # Roles default to None when another player becomes a Tanner and realizes it
        super().__init__(player_index)
        self.role = 'Tanner'
        self.statements = []
        self.new_role = ''

    def get_statement(self, stated_roles=None, previous=None):
        ''' Get Tanner Statement. '''
        return None

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
        return val
