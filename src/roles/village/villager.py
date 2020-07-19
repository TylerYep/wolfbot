""" villager.py """
from __future__ import annotations

from typing import List, Tuple

from overrides import overrides

from src.roles.player import Player
from src.statements import Statement


class Villager(Player):
    """ Villager Player class. """

    def __init__(self, player_index: int):
        super().__init__(player_index)
        self.statements += self.get_villager_statements(player_index)

    @classmethod
    @overrides
    def awake_init(
        cls, player_index: int, game_roles: List[str], original_roles: List[str]
    ) -> Villager:
        """ Initializes Villager when night falls. """
        del game_roles, original_roles
        return cls(player_index)

    @staticmethod
    def get_villager_statements(player_index: int) -> Tuple[Statement, ...]:
        """ Gets Villager Statements. """
        return (Statement("I am a Villager.", ((player_index, frozenset({"Villager"})),)),)

    @staticmethod
    @overrides
    def get_all_statements(player_index: int) -> Tuple[Statement, ...]:
        """ Required for all player types. Returns all possible role statements. """
        return Villager.get_villager_statements(player_index)
