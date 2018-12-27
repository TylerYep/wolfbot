''' wolf.py '''
import random

from algorithms import switching_solver
from predictions import make_prediction_fast
from const import logger
import const
import util

from ..village import Player
from .wolf_variants import get_wolf_statements_random, get_statement_expectimax, \
                           get_statement_rl, get_wolf_statements, get_center_wolf_statements

class Wolf(Player):
    ''' Wolf Player class. '''

    def __init__(self, player_index, game_roles=None, original_roles=None):
        '''
        Constructor: original_roles defaults to None when a player becomes a Wolf and realizes it.
        '''
        super().__init__(player_index)
        self.role = 'Wolf'
        self.wolf_indices, self.center_index, self.center_role \
                = self.wolf_init(game_roles, original_roles)

    def wolf_init(self, game_roles, original_roles):
        ''' Initializes Wolf - gets Wolf indices and a random center card, if applicable. '''
        wolf_indices = []
        wolf_center_index, wolf_center_role = None, None

        # Only get center roles and wolf indices if not a Robber/Insomniac Wolf
        if original_roles is not None:
            wolf_indices = set(util.find_all_player_indices(original_roles, 'Wolf'))
            if len(wolf_indices) == 1 and const.NUM_CENTER > 0:
                wolf_center_index = util.get_center(self)
                wolf_center_role = game_roles[wolf_center_index]
            logger.debug('[Hidden] Wolves are at indices: %s', str(wolf_indices))
            if self.is_user: logger.info('Wolves are at indices: %s', str(wolf_indices))

        return wolf_indices, wolf_center_index, wolf_center_role

    def get_statement(self, stated_roles, previous):
        ''' Get Wolf Statement. '''
        if const.USE_REG_WOLF:
            if self.center_role not in (None, 'Wolf', 'Mason'):
                self.statements = get_center_wolf_statements(self, stated_roles)
            if not self.statements:
                self.statements = get_wolf_statements(self, stated_roles, previous)
        else:
            self.statements = get_wolf_statements_random(self)

        # Choose one statement to return by default
        if const.USE_RL_WOLF:
            return get_statement_rl(self, stated_roles, previous, super().get_statement())

        if const.USE_EXPECTIMAX_WOLF:
            return get_statement_expectimax(self, previous)

        return super().get_statement(stated_roles, previous)

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
        for wolfi in self.wolf_indices:
            if predictions[wolfi] == 'Wolf':
                val -= 5
            if 'Wolf' in solver_result.possible_roles[wolfi]:
                val -= 5
        return val
