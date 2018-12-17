''' minion.py '''
from util import find_all_player_indices
from const import logger
import const

from ..village import Player
from .wolf import Wolf
# TODO TRIM THESE
from .wolf_variants import get_wolf_statements_random, get_statement_expectimax, \
                           get_statement_rl, get_wolf_statements, get_center_wolf_statements

class Minion(Player):
    ''' Minion Player class. '''

    def __init__(self, player_index, game_roles, ORIGINAL_ROLES=None):
        # Roles default to None when another player becomes a Minion and realizes it
        super().__init__(player_index)
        self.role = 'Minion'
        self.statements = []
        self.wolf_indices = self.minion_init(ORIGINAL_ROLES)
        self.new_role = ''

    def minion_init(self, ORIGINAL_ROLES):
        ''' Initializes Minion - gets Wolf indices. '''
        wolf_indices = []
        if ORIGINAL_ROLES is not None:
            wolf_indices = set(find_all_player_indices(ORIGINAL_ROLES, 'Wolf'))
        logger.debug('[Hidden] Wolves are at indices: %s', str(wolf_indices))
        return wolf_indices

    def get_statement(self, stated_roles, previous_statements):
        ''' Get Minion Statement. '''
        return get_statement_expectimax(self.eval_fn, self.player_index, previous_statements,
                                        possible_statements, self.wolf_indices)

    def eval_fn(statement_list):
        '''
        Evaluates a complete or incomplete game.
        # wolves in a positions - # of ones that are actually wolves, size of set
        '''
        solver_result = random.choice(switching_solver(statement_list))
        predictions = make_prediction_fast(solver_result)
        val = 10
        if not predictions:
            return -10
        for wolfi in wolf_indices:
            if predictions[wolfi] == 'Wolf':
                val -= 5
            if 'Wolf' in solver_result.possible_roles[wolfi]:
                val -= 5
        return val