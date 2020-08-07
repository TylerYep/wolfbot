""" hunter.py """
from __future__ import annotations

from typing import List, Tuple

from src.const import Role, RoleBits, lru_cache
from src.roles.player import Player
from src.statements import Statement


class Hunter(Player):
    """ Hunter Player class. """

    def __init__(self, player_index: int):
        super().__init__(player_index)
        self.statements += self.get_hunter_statements(player_index)

    @classmethod
    def awake_init(
        cls, player_index: int, game_roles: List[Role], original_roles: Tuple[Role, ...]
    ) -> Hunter:
        """ Initializes Hunter when night falls. """
        del game_roles, original_roles
        return cls(player_index)

    @staticmethod
    @lru_cache
    def get_hunter_statements(player_index: int) -> Tuple[Statement, ...]:
        """ Gets Hunter Statement. """
        return (Statement("I am a Hunter.", ((player_index, RoleBits.from_roles(Role.HUNTER)),)),)

    @staticmethod
    @lru_cache
    def get_all_statements(player_index: int) -> Tuple[Statement, ...]:
        """ Required for all player types. Returns all possible role statements. """
        return Hunter.get_hunter_statements(player_index)
