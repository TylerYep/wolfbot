from __future__ import annotations

from typing import Any, Self, override

from wolfbot import const
from wolfbot.enums import Role, lru_cache
from wolfbot.game_utils import find_all_player_indices
from wolfbot.log import logger
from wolfbot.roles.player import Player
from wolfbot.statements import Statement


class Mason(Player):
    """Mason Player class."""

    def __init__(self, player_index: int, mason_indices: tuple[int, ...]) -> None:
        super().__init__(player_index)
        self.mason_indices = mason_indices
        self.statements += self.get_mason_statements(player_index, mason_indices)
        if self.player_index not in self.mason_indices:
            raise RuntimeError("Player index is not one of the Mason indices.")

    @classmethod
    @override
    def awake_init(cls, player_index: int, game_roles: list[Role]) -> Self:
        """Initializes Mason - sees all other Masons."""
        is_user = const.IS_USER[player_index]
        mason_indices = find_all_player_indices(game_roles, Role.MASON)
        logger.debug(f"[Hidden] Masons are at indices: {list(mason_indices)}")
        if is_user:
            logger.info(
                f"Masons are players: {list(mason_indices)} "
                f"(You are player {player_index})",
                cache=True,
            )
        return cls(player_index, mason_indices)

    @staticmethod
    @lru_cache
    def get_mason_statements(
        player_index: int, mason_indices: tuple[int, ...]
    ) -> tuple[Statement, ...]:
        """Gets Mason Statement."""
        if len(mason_indices) == 1:
            sentence = "I am a Mason. The other Mason is not present."
            knowledge = [(player_index, frozenset({Role.MASON}))] + [
                (ind, const.ROLE_SET - frozenset({Role.MASON}))
                for ind in range(const.NUM_PLAYERS)
                if ind != player_index
            ]
        else:
            other_mason = (
                mason_indices[0]
                if mason_indices[0] != player_index
                else mason_indices[1]
            )
            sentence = f"I am a Mason. The other Mason is Player {other_mason}."
            knowledge = [
                (player_index, frozenset({Role.MASON})),
                (other_mason, frozenset({Role.MASON})),
            ]
        return (Statement(sentence, tuple(knowledge)),)

    @staticmethod
    @lru_cache
    @override
    def get_all_statements(player_index: int) -> tuple[Statement, ...]:
        """Required for all player types. Returns all possible role statements."""
        statements = Mason.get_mason_statements(player_index, (player_index,))
        for i in range(const.NUM_PLAYERS):
            if player_index != i:
                mason_indices = (player_index, i)
                statements += Mason.get_mason_statements(player_index, mason_indices)
        return statements

    @override
    def json_repr(self) -> dict[str, Any]:
        """Gets JSON representation of a Mason player."""
        return super().json_repr() | {"mason_indices": self.mason_indices}
