''' robber.py '''
from typing import List, Tuple

from src.statements import Statement
from src.const import logger
from src import const, util

from .player import Player

class Robber(Player):
    ''' Robber Player class. '''

    def __init__(self, player_index: int, game_roles: List[str], original_roles: List[str]):
        super().__init__(player_index)
        self.choice_ind, choice_char = self.robber_init(game_roles)
        self.new_role = choice_char
        self.statements = self.get_robber_statements(player_index, self.choice_ind, choice_char)

    def robber_init(self, game_roles: List[str]) -> Tuple[int, str]:
        ''' Initializes Robber - switches roles with another player. '''
        choice_ind = util.get_player(self.is_user, (self.player_index,))
        choice_char = game_roles[choice_ind]
        logger.debug(f'[Hidden] Robber switches with Player {choice_ind}'
                     f' and becomes a {choice_char}.')
        util.swap_characters(game_roles, self.player_index, choice_ind)
        return choice_ind, choice_char

    @staticmethod
    def get_robber_statements(player_index: int,
                              choice_ind: int,
                              choice_char: str) -> List[Statement]:
        ''' Gets Robber Statement. '''
        sentence = (f'I am a Robber and I swapped with Player {choice_ind}. '
                    f'I am now a {choice_char}.')
        knowledge = [(player_index, {'Robber'}), (choice_ind, {choice_char})]
        switches = [(const.ROBBER_PRIORITY, player_index, choice_ind)]
        return [Statement(sentence, knowledge, switches)]

    @staticmethod
    def get_all_statements(player_index: int) -> List[Statement]:
        ''' Required for all player types. Returns all possible role statements. '''
        statements = []
        for i in range(const.NUM_PLAYERS):
            for role in const.ROLE_SET:
                if player_index != i:      # OK: 'I robbed Player 0 and now I'm a Wolf... ;)'
                    statements += Robber.get_robber_statements(player_index, i, role)
        return statements

    def get_statement(self, stated_roles: List[str], previous: List[Statement]) -> Statement:
        ''' Overrides get_statement when the Insomniac becomes a Wolf. '''
        if self.new_role == 'Wolf':
            # Import Wolf here to avoid circular dependency
            from ..werewolf import Wolf
            logger.debug('Robber is a Wolf now!')
            robber_wolf = Wolf(self.player_index, [], [])
            return robber_wolf.get_statement(stated_roles, previous)

        if self.new_role == 'Minion':
            # Import Minion here to avoid circular dependency
            from ..werewolf import Minion
            logger.debug('Robber is a Minion now!')
            robber_minion = Minion(self.player_index, [], [])
            return robber_minion.get_statement(stated_roles, previous)

        if self.new_role == 'Tanner':
            # Import Tanner here to avoid circular dependency
            from ..werewolf import Tanner
            logger.debug('Robber is a Minion now!')
            robber_tanner = Tanner(self.player_index, [], [])
            return robber_tanner.get_statement(stated_roles, previous)

        return super().get_statement(stated_roles, previous)
