''' seer.py '''
import random

from src.statements import Statement
from src.const import logger
from src import const, util

from .player import Player

class Seer(Player):
    ''' Seer Player class. '''

    def __init__(self, player_index, game_roles, original_roles):
        super().__init__(player_index)
        peek_ind, peek_char, peek_ind2, peek_char2 = self.seer_init(game_roles)
        self.statements = self.get_seer_statements(player_index, peek_ind, peek_char,
                                                   peek_ind2, peek_char2)

    def seer_init(self, game_roles):
        ''' Initializes Seer - either sees 2 center cards or 1 player card. '''
        # Pick two center cards more often, because that generally yields higher win rates.
        choose_center = random.choices([True, False], [0.9, 0.1])
        if choose_center and const.NUM_CENTER > 1:
            peek_ind = util.get_center(self)
            peek_ind2 = util.get_center(self, [peek_ind])
            peek_char = game_roles[peek_ind]
            peek_char2 = game_roles[peek_ind2]
            logger.debug(f'[Hidden] Seer sees that Center {peek_ind - const.NUM_PLAYERS} is a '
                         f'{peek_char}, Center {peek_ind2 - const.NUM_PLAYERS} is a {peek_char2}.')
            return peek_ind, peek_char, peek_ind2, peek_char2

        peek_ind = util.get_player(self, [self.player_index])
        peek_char = game_roles[peek_ind]
        logger.debug(f'[Hidden] Seer sees that Player {peek_ind} is a {peek_char}.')
        return peek_ind, peek_char, None, None

    @staticmethod
    def get_seer_statements(player_index, seen_index, seen_role, seen_index2=None, seen_role2=None):
        ''' Gets Seer Statement. '''
        sentence = f'I am a Seer and I saw that Player {seen_index} was a {seen_role}.'
        knowledge = [(player_index, {'Seer'}), (seen_index, {seen_role})]
        if seen_index2 is not None:
            sentence = f'I am a Seer and I saw that Center {seen_index - const.NUM_PLAYERS} was a' \
                       + f' {seen_role} and that Center {seen_index2 - const.NUM_PLAYERS}' \
                       + f' was a {seen_role2}.'
            knowledge.append((seen_index2, {seen_role2}))
        return [Statement(sentence, knowledge)]

    @staticmethod
    def get_all_statements(player_index):
        ''' Required for all player types. Returns all possible role statements. '''
        statements = []
        for role in const.ROLES:
            for i in range(const.NUM_PLAYERS):   # OK: 'Hey, I'm a Seer and I saw another Seer...'
                statements += Seer.get_seer_statements(player_index, i, role)
        # Wolf using these usually gives himself away
        for cent1 in range(const.NUM_CENTER):
            for cent2 in range(cent1 + 1, const.NUM_CENTER):
                for role1 in const.ROLE_SET - {'Seer'}:
                    for role2 in const.ROLE_SET - {'Seer'}:
                        if role1 != role2 or const.ROLE_COUNTS[role1] >= 2:
                            statements += Seer.get_seer_statements(player_index,
                                                                   cent1 + const.NUM_PLAYERS, role1,
                                                                   cent2 + const.NUM_PLAYERS, role2)
        return statements
