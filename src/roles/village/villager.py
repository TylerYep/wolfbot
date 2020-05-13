""" villager.py """
from __future__ import annotations

from typing import Any, Dict, List

from src.statements import Statement

from ..player import Player


class Villager(Player):
    """ Villager Player class. """

    def __init__(self, player_index: int):
        super().__init__(player_index)
        self.statements += self.get_villager_statements(player_index)

    @classmethod
    def awake_init(
        cls, player_index: int, game_roles: List[str], original_roles: List[str]
    ) -> Villager:
        """ Initializes Villager when night falls. """
        del game_roles, original_roles
        return cls(player_index)

    @staticmethod
    def get_villager_statements(player_index: int) -> List[Statement]:
        """ Gets Villager Statements. """
        return [Statement("I am a Villager.", ((player_index, frozenset({"Villager"})),))]

    @staticmethod
    def get_all_statements(player_index: int) -> List[Statement]:
        """ Required for all player types. Returns all possible role statements. """
        return Villager.get_villager_statements(player_index)

    def json_repr(self) -> Dict[str, Any]:
        """ Gets JSON representation of a Villager player. """
        return {"type": self.role, "player_index": self.player_index}
