from __future__ import annotations

from wolfbot.enums import Role, lru_cache
from wolfbot.roles.player import Player
from wolfbot.statements import Statement


class Villager(Player):
    """Villager Player class."""

    def __init__(self, player_index: int):
        super().__init__(player_index)
        self.statements += self.get_villager_statements(player_index)

    @classmethod
    def awake_init(
        cls, player_index: int, game_roles: list[Role], original_roles: tuple[Role, ...]
    ) -> Villager:
        """Initializes Villager when night falls."""
        del game_roles, original_roles
        return cls(player_index)

    @staticmethod
    @lru_cache
    def get_villager_statements(player_index: int) -> tuple[Statement, ...]:
        """Gets Villager Statements."""
        return (
            Statement(
                "I am a Villager.", ((player_index, frozenset({Role.VILLAGER})),)
            ),
        )

    @staticmethod
    @lru_cache
    def get_all_statements(player_index: int) -> tuple[Statement, ...]:
        """Required for all player types. Returns all possible role statements."""
        return Villager.get_villager_statements(player_index)
