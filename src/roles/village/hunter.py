""" hunter.py """
from __future__ import annotations

from typing import Any, Dict, List

from src.statements import Statement

from ..player import Player


class Hunter(Player):
    """ Hunter Player class. """

    def __init__(self, player_index: int):
        super().__init__(player_index)
        self.statements += self.get_hunter_statements(player_index)

    @classmethod
    def awake_init(
        cls, player_index: int, game_roles: List[str], original_roles: List[str]
    ) -> Hunter:
        """ Initializes Hunter when night falls. """
        del game_roles, original_roles
        return cls(player_index)

    @staticmethod
    def get_hunter_statements(player_index: int) -> List[Statement]:
        """ Gets Hunter Statement. """
        return [Statement("I am a Hunter.", [(player_index, {"Hunter"})])]

    @staticmethod
    def get_all_statements(player_index: int) -> List[Statement]:
        """ Required for all player types. Returns all possible role statements. """
        return Hunter.get_hunter_statements(player_index)

    def json_repr(self) -> Dict[str, Any]:
        """ Gets JSON representation of a Hunter player. """
        return {"type": self.role, "player_index": self.player_index}
