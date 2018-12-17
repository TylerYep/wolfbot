''' seer.py '''
import random

from statements import Statement
from util import get_random_center, get_random_player
from const import logger
import const

from .player import Player

class Seer(Player):
    ''' Seer Player class. '''

    def __init__(self, player_index, game_roles, original_roles):
        super().__init__(player_index)
        seer_peek_index, seer_peek_character, \
            seer_peek_index2, seer_peek_character2 = self.seer_init(player_index, game_roles)
        self.role = 'Seer'
        self.statements = self.get_seer_statements(player_index, seer_peek_index, seer_peek_character,
                                                   seer_peek_index2, seer_peek_character2)

    @staticmethod
    def seer_init(player_index, game_roles):
        ''' Initializes Seer - either sees 2 center cards or 1 player card. '''
        # Pick two center cards more often, because that generally yields higher win rates.
        choose_center = random.choices([True, False], [0.9, 0.1])
        if choose_center and const.NUM_CENTER > 1:
            seer_peek_index = get_random_center()
            seer_peek_character = game_roles[seer_peek_index]
            seer_peek_index2 = get_random_center()
            while seer_peek_index2 == seer_peek_index:
                seer_peek_index2 = get_random_center()
            seer_peek_character2 = game_roles[seer_peek_index2]
            logger.debug('[Hidden] Seer sees that Center %d is a %s and Center %d is a %s.',
                         seer_peek_index - const.NUM_PLAYERS, str(seer_peek_character),
                         seer_peek_index2 - const.NUM_PLAYERS, str(seer_peek_character2))
            return seer_peek_index, seer_peek_character, seer_peek_index2, seer_peek_character2

        seer_peek_index = get_random_player()
        while seer_peek_index == player_index:
            seer_peek_index = get_random_player()
        seer_peek_character = game_roles[seer_peek_index]
        logger.debug('[Hidden] Seer sees that Player %d is a %s.',
                     seer_peek_index, str(seer_peek_character))
        return seer_peek_index, seer_peek_character, None, None

    @staticmethod
    def get_seer_statements(player_index, seen_index, seen_role, seen_index2=None, seen_role2=None):
        ''' Gets Seer Statement. '''
        sentence = 'I am a Seer and I saw that Player ' + str(seen_index) + ' was a ' + str(seen_role) + '.'
        knowledge = [(player_index, {'Seer'}), (seen_index, {seen_role})]
        if seen_index2 is not None:
            sentence = 'I am a Seer and I saw that Center ' + str(seen_index - const.NUM_PLAYERS) \
                        + ' was a ' + str(seen_role) + ' and that Center ' \
                        + str(seen_index2 - const.NUM_PLAYERS) + ' was a ' + str(seen_role2) + '.'
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
                            statements += Seer.get_seer_statements(player_index, cent1 + const.NUM_PLAYERS,
                                                                   role1, cent2 + const.NUM_PLAYERS, role2)
        return statements
