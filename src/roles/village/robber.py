''' robber.py '''
import random

from statements import Statement
from util import get_random_player, swap_characters
from const import logger
import const

from .player import Player

class Robber(Player):
    ''' Robber Player class. '''

    def __init__(self, player_index, game_roles, original_roles):
        super().__init__(player_index)
        robber_choice_index, robber_choice_character = self.robber_init(player_index, game_roles)
        self.role = 'Robber'
        self.new_role = robber_choice_character
        self.statements = self.get_robber_statements(player_index, robber_choice_index,
                                                     robber_choice_character)

    @staticmethod
    def robber_init(player_index, game_roles):
        ''' Initializes Robber - switches roles with another player. '''
        robber_choice_index = get_random_player()
        while robber_choice_index == player_index:
            robber_choice_index = get_random_player()
        robber_choice_character = game_roles[robber_choice_index]
        logger.debug('[Hidden] Robber switches with Player %d and becomes a %s.',
                     robber_choice_index, str(robber_choice_character))
        swap_characters(game_roles, player_index, robber_choice_index)
        return robber_choice_index, robber_choice_character

    @staticmethod
    def get_robber_statements(player_index, robber_choice_index, robber_choice_character):
        ''' Gets Robber Statement. '''
        sentence = 'I am a Robber and I swapped with Player ' + str(robber_choice_index) \
                    + '. I am now a ' + robber_choice_character + '.'
        knowledge = [(player_index, {'Robber'}), (robber_choice_index, {robber_choice_character})]
        switches = [(const.ROBBER_PRIORITY, robber_choice_index, player_index)]
        return [Statement(sentence, knowledge, switches)]

    @staticmethod
    def get_all_statements(player_index):
        ''' Required for all player types. Returns all possible role statements. '''
        statements = []
        for i in range(const.NUM_PLAYERS):
            for role in const.ROLES:
                if player_index != i:      # OK: 'I robbed Player 0 and now I'm a Wolf... ;)'
                    statements += Robber.get_robber_statements(player_index, i, role)
        return statements

    def get_statement(self, stated_roles=None, previous=None):
        ''' Overrides get_statement when the Insomniac becomes a Wolf. '''
        if self.new_role == 'Wolf':
            # Import Wolf here to avoid circular dependency
            from ..werewolf import Wolf
            logger.debug('Robber is a Wolf now!')
            robber_wolf = Wolf(self.player_index)
            return robber_wolf.get_statement(stated_roles, previous)

        if self.new_role == 'Minion':
            # Import Minion here to avoid circular dependency
            from ..werewolf import Minion
            logger.debug('Robber is a Minion now!')
            robber_minion = Minion(self.player_index, None)
            return robber_minion.get_statement(stated_roles, previous)

        if self.new_role == 'Tanner':
            # Import Tanner here to avoid circular dependency
            from ..werewolf import Tanner
            logger.debug('Robber is a Minion now!')
            robber_tanner = Tanner(self.player_index, None)
            return robber_tanner.get_statement(stated_roles, previous)

        return random.choice(tuple(self.statements))
