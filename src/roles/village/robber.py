from .player import Player
from statements import Statement
from util import get_random_player, swap_characters
from const import logger
import const
import random

class Robber(Player):
    def __init__(self, player_index, game_roles, ORIGINAL_ROLES):
        super().__init__(player_index)
        robber_choice_index, robber_choice_character = self.robber_init(game_roles)
        self.role = 'Robber'
        self.new_role = robber_choice_character
        self.statements = self.get_robber_statements(player_index, robber_choice_index, robber_choice_character)

    def robber_init(self, game_roles):
        ''' Initializes Robber - switches roles with another player. '''
        robber_choice_index = get_random_player()
        while robber_choice_index == self.player_index:
            robber_choice_index = get_random_player()
        robber_choice_character = game_roles[robber_choice_index]
        logger.debug('[Hidden] Robber switches with Player ' + str(robber_choice_index) +
                    ' and becomes a ' + str(robber_choice_character))
        swap_characters(game_roles, self.player_index, robber_choice_index)
        return robber_choice_index, robber_choice_character

    @staticmethod
    def get_robber_statements(player_index, robber_choice_index, robber_choice_character):
        sentence = 'I am a Robber and I swapped with Player ' + str(robber_choice_index) + \
                    '. I am now a ' + robber_choice_character + '.'
        knowledge = [(player_index, {'Robber'}), (robber_choice_index, {robber_choice_character})]
        switches = [(const.ROBBER_PRIORITY, robber_choice_index, player_index)]
        return [Statement(sentence, knowledge, switches)]

    def get_statement(self, stated_roles, previous):
        if self.new_role == 'Wolf':
            # Import Wolf here to avoid circular dependency
            from ..werewolf import Wolf
            logger.debug('Robber is a Wolf now!')
            robber_wolf = Wolf(self.player_index)
            return robber_wolf.get_statement(stated_roles, previous)
        else:
            return random.choice(tuple(self.statements))
