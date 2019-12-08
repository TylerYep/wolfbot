''' player.py '''
from typing import Any, Dict, List
import random

from src import const, util
from src.const import logger
from src.statements import Statement
from src.algorithms import switching_solver

class Player:
    ''' Player class. '''

    def __init__(self, player_index: int, new_role: str = ''):
        self.player_index = player_index
        self.role = type(self).__name__  # e.g. 'Wolf'
        self.new_role = new_role
        self.statements: List[Statement] = []
        self.is_user = const.IS_USER[player_index]

    def transform(self, role_type: str) -> Any:
        ''' Returns new Player identity. '''
        from .werewolf import Wolf, Minion, Tanner
        from .village import Villager, Seer, Robber, Troublemaker, Drunk, Insomniac, Hunter, Mason
        logger.debug(f'[Hidden] {self.role} is a {role_type} now!')

        if role_type == 'Wolf':
            return Wolf(self.player_index, [])
        if role_type == 'Minion':
            return Minion(self.player_index, [])
        if role_type == 'Tanner':
            return Tanner(self.player_index)
        if role_type == 'Villager':
            return Villager(self.player_index)
        if role_type == 'Hunter':
            return Hunter(self.player_index)
        # Made-up parameters
        if role_type == 'Seer':
            return Seer(self.player_index, (0, 'Villager'))
        if role_type == 'Robber':
            return Robber(self.player_index, 0, 'Villager')
        if role_type == 'Troublemaker':
            return Troublemaker(self.player_index, 0, 1)
        if role_type == 'Drunk':
            return Drunk(self.player_index, const.NUM_PLAYERS + 1)
        if role_type == 'Insomniac':
            return Insomniac(self.player_index, 'Insomniac')
        if role_type == 'Mason':
            return Mason(self.player_index, [0, 1])
        return None

    def get_statement(self, stated_roles: List[str], previous: List[Statement]) -> Statement:
        ''' Gets Player Statement. '''
        if self.is_user:
            logger.info('Please choose from the following statements: ')
            sample_statements = random.sample(self.statements, 10) if len(self.statements) > 10 \
                                else self.statements
            for i, statement in enumerate(sample_statements):
                logger.info(f'{i}. {statement.sentence}')
            choice = util.get_numeric_input(len(sample_statements))
            return sample_statements[choice]

        if self.role in const.VILLAGE_ROLES:
            # TODO Want to use random solution but would break tests.
            solver_result = switching_solver(tuple(previous))[0]
            for i, truth in enumerate(solver_result.path):
                if truth:
                    statement = previous[i]
                    ref = statement.get_references(self.player_index)
                    if ref is not None:
                        if isinstance(ref, frozenset) and len(ref) == 1:
                            [self.new_role] = ref
                        elif isinstance(ref, int):
                            switched_index = ref
                            if switched_index < len(stated_roles):
                                self.new_role = stated_roles[switched_index]

        if self.new_role != '' and self.new_role in const.EVIL_ROLES:
            return self.transform(self.new_role).get_statement(stated_roles, previous)

        return random.choice(tuple(self.statements))

    def __eq__(self, other) -> bool:
        ''' Checks for equality between Players. '''
        assert isinstance(other, Player)
        self_json, other_json = self.json_repr(), other.json_repr()
        is_equal = all([self_json[key] == other_json[key] for key in self_json])
        return self.__dict__ == other.__dict__ and is_equal

    def json_repr(self) -> Dict:
        ''' Gets JSON representation of a Player object. '''
        return {'type': self.role, 'player_index': self.player_index}

    def __repr__(self) -> str:
        ''' Gets string representation of a Player object. '''
        attrs = ''
        for key, item in self.json_repr().items():
            if key != 'type':
                attrs += f'{item}, '
        return f'{self.role}({attrs[:-2]})'
