from __future__ import annotations

from typing import Any, Self, override

from wolfbot import const
from wolfbot.enums import Role, SwitchPriority, lru_cache
from wolfbot.game_utils import get_center, swap_characters
from wolfbot.log import logger
from wolfbot.roles.player import Player
from wolfbot.statements import Statement


class Drunk(Player):
    """Drunk Player class."""

    def __init__(self, player_index: int, choice_ind: int) -> None:
        super().__init__(player_index)
        self.choice_ind = choice_ind
        self.statements += self.get_drunk_statements(player_index, choice_ind)

    @classmethod
    @override
    def awake_init(cls, player_index: int, game_roles: list[Role]) -> Self:
        """Initializes Drunk - switches with a card in the center."""
        is_user = const.IS_USER[player_index]
        choice_ind = get_center(is_user)
        logger.debug(
            f"[Hidden] Drunk switches with Center Card {choice_ind - const.NUM_PLAYERS}"
            f" and unknowingly becomes a {game_roles[choice_ind]}."
        )
        if is_user:
            logger.info("You do not know your new role.", cache=True)
        swap_characters(game_roles, player_index, choice_ind)
        return cls(player_index, choice_ind)

    @staticmethod
    @lru_cache
    def get_drunk_statements(
        player_index: int, choice_ind: int
    ) -> tuple[Statement, ...]:
        """Gets Drunk Statement."""
        sentence = (
            f"I am a Drunk and I swapped with Center {choice_ind - const.NUM_PLAYERS}."
        )
        knowledge = ((player_index, frozenset({Role.DRUNK})),)
        switches = ((SwitchPriority.DRUNK, player_index, choice_ind),)
        return (Statement(sentence, knowledge, switches),)

    @staticmethod
    @lru_cache
    @override
    def get_all_statements(player_index: int) -> tuple[Statement, ...]:
        """Required for all player types. Returns all possible role statements."""
        statements: tuple[Statement, ...] = ()
        for k in range(const.NUM_CENTER):
            statements += Drunk.get_drunk_statements(
                player_index, const.NUM_PLAYERS + k
            )
        return statements

    @override
    def json_repr(self) -> dict[str, Any]:
        """Gets JSON representation of a Drunk player."""
        return super().json_repr() | {"choice_ind": self.choice_ind}
