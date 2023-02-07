from __future__ import annotations

from typing import Self

from wolfbot.enums import Role, lru_cache
from wolfbot.roles.player import Player
from wolfbot.statements import Statement


class Hunter(Player):
    """Hunter Player class."""

    def __init__(self, player_index: int):
        super().__init__(player_index)
        self.statements += self.get_hunter_statements(player_index)

    @classmethod
    def awake_init(cls, player_index: int, game_roles: list[Role]) -> Self:
        """Initializes Hunter when night falls."""
        del game_roles
        return cls(player_index)

    @staticmethod
    @lru_cache
    def get_hunter_statements(player_index: int) -> tuple[Statement, ...]:
        """Gets Hunter Statement."""
        return (
            Statement("I am a Hunter.", ((player_index, frozenset({Role.HUNTER})),)),
        )

    @staticmethod
    @lru_cache
    def get_all_statements(player_index: int) -> tuple[Statement, ...]:
        """Required for all player types. Returns all possible role statements."""
        return Hunter.get_hunter_statements(player_index)
