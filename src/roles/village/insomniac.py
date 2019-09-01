''' insomniac.py '''
from typing import List, Optional

from src.statements import Statement
from src.const import logger
from src import const

from .player import Player

class Insomniac(Player):
    ''' Insomniac Player class. '''

    def __init__(self, player_index: int, game_roles: List[str], original_roles: List[str]):
        super().__init__(player_index)
        insomniac_new_role = self.insomniac_init(game_roles)
        self.new_role = insomniac_new_role
        self.statements = self.get_insomniac_statements(player_index, insomniac_new_role)

    def insomniac_init(self, game_roles: List[str]) -> str:
        ''' Initializes Insomniac - learns new role. '''
        insomniac_new_role = game_roles[self.player_index]
        logger.debug(f'[Hidden] Insomniac wakes up as a {insomniac_new_role}.')
        if self.is_user: logger.info(f'You woke up as a {insomniac_new_role}!')
        return insomniac_new_role

    @staticmethod
    def get_insomniac_statements(player_index: int,
                                 insomniac_new_role: str,
                                 new_insomniac_index: Optional[int] = None) -> List[Statement]:
        ''' Gets Insomniac Statement. '''
        knowledge = [(player_index, {'Insomniac'})]
        sentence = f'I am a Insomniac and when I woke up I was a {insomniac_new_role}.'
        if new_insomniac_index is None:
            if insomniac_new_role != 'Insomniac':
                sentence += ' I don\'t know who I switched with.'
        else:
            sentence += f' I switched with Player {new_insomniac_index}.'
        # switches = [(player_index, new_insomniac_index)]  # TODO
        return [Statement(sentence, knowledge)]

    @staticmethod
    def get_all_statements(player_index: int) -> List[Statement]:
        ''' Required for all player types. Returns all possible role statements. '''
        statements = []
        for role in const.ROLES:
            statements += Insomniac.get_insomniac_statements(player_index, role)
        return statements

    def get_statement(self, stated_roles: List[str], previous: List[Statement]) -> Statement:
        ''' Overrides get_statement when the Insomniac becomes a Wolf. '''
        if self.new_role == 'Wolf':
            # Import Wolf here to avoid circular dependency
            from ..werewolf import Wolf
            logger.debug('Insomniac is a Wolf now!')
            insomniac_wolf = Wolf(self.player_index)
            return insomniac_wolf.get_statement(stated_roles, previous)

        if self.new_role == 'Minion':
            # Import Minion here to avoid circular dependency
            from ..werewolf import Minion
            logger.debug('Insomniac is a Minion now!')
            insomniac_minion = Minion(self.player_index, None)
            return insomniac_minion.get_statement(stated_roles, previous)

        if self.new_role == 'Tanner':
            # Import Tanner here to avoid circular dependency
            from ..werewolf import Tanner
            logger.debug('Insomniac is a Minion now!')
            insomniac_tanner = Tanner(self.player_index, None)
            return insomniac_tanner.get_statement(stated_roles, previous)

        possible_switches = []
        for i, stated_role in enumerate(stated_roles):
            if stated_role == self.new_role:
                possible_switches.append(i)
        if len(possible_switches) == 1: # TODO how to handle multiple possible switches
            self.statements = self.get_insomniac_statements(self.player_index, self.new_role,
                                                            possible_switches[0])
        return super().get_statement(stated_roles, previous)
