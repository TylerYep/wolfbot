''' insomniac.py '''
import random

from statements import Statement
from const import logger
import const

from .player import Player

class Insomniac(Player):
    ''' Insomniac Player class. '''

    def __init__(self, player_index, game_roles, ORIGINAL_ROLES):
        super().__init__(player_index)
        insomniac_new_role = self.insomniac_init(player_index, game_roles)
        self.role = 'Insomniac'
        self.new_role = insomniac_new_role
        self.statements = self.get_insomniac_statements(player_index, insomniac_new_role)

    @staticmethod
    def insomniac_init(player_index, game_roles):
        ''' Initializes Insomniac - learns new role. '''
        insomniac_new_role = game_roles[player_index]
        logger.debug('[Hidden] Insomniac wakes up as a %s.', insomniac_new_role)
        return insomniac_new_role

    @staticmethod
    def get_insomniac_statements(player_index, insomniac_new_role, new_insomniac_index=None):
        ''' Gets Insomniac Statement. '''
        knowledge = [(player_index, {'Insomniac'})]
        sentence = 'I am a Insomniac and when I woke up I was a ' + str(insomniac_new_role) + '.'
        if new_insomniac_index is None:
            if insomniac_new_role != 'Insomniac':
                sentence += ' I don\'t know who I switched with.'
        else:
            sentence += ' I switched with Player ' + str(new_insomniac_index) + '.'
        # switches = [(player_index, new_insomniac_index)]  # TODO
        return [Statement(sentence, knowledge)]

    @staticmethod
    def get_all_statements(player_index):
        ''' Required for all player types. Returns all possible role statements. '''
        statements = []
        for role in const.ROLES:
            statements += Insomniac.get_insomniac_statements(player_index, role)
        return statements

    def get_statement(self, stated_roles=None, previous=None):
        ''' Overrides get_statement when the Insomniac becomes a Wolf. '''
        if self.new_role == 'Wolf':
            # Import Wolf here to avoid circular dependency
            from ..werewolf import Wolf
            logger.debug('Insomniac is a Wolf now!')
            insomniac_wolf = Wolf(self.player_index)
            return insomniac_wolf.get_statement(stated_roles, previous)

        possible_switches = []
        for i, stated_role in enumerate(stated_roles):
            if stated_role == self.new_role:
                possible_switches.append(i)
        if len(possible_switches) == 1: # TODO how to handle multiple possible switches
            self.statements = self.get_insomniac_statements(self.player_index, self.new_role,
                                                            possible_switches[0])
        return random.choice(tuple(self.statements))
