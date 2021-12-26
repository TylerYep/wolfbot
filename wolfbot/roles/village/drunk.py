from __future__ import annotations

from typing import Any

from wolfbot import const, util
from wolfbot.enums import Role, SwitchPriority, lru_cache
from wolfbot.log import logger
from wolfbot.roles.player import Player
from wolfbot.statements import Statement
from wolfbot.user import get_center


class Drunk(Player):
    """Drunk Player class."""

    def __init__(self, player_index: int, choice_ind: int):
        super().__init__(player_index)
        self.choice_ind = choice_ind
        self.statements += self.get_drunk_statements(player_index, choice_ind)

    @classmethod
    def awake_init(
        cls, player_index: int, game_roles: list[Role], original_roles: tuple[Role, ...]
    ) -> Drunk:
        """Initializes Drunk - switches with a card in the center."""
        del original_roles
        is_user = const.IS_USER[player_index]
        choice_ind = get_center(is_user)
        logger.debug(
            f"[Hidden] Drunk switches with Center Card {choice_ind - const.NUM_PLAYERS}"
            f" and unknowingly becomes a {game_roles[choice_ind]}."
        )
        if is_user:
            logger.info("You do not know your new role.", cache=True)
        util.swap_characters(game_roles, player_index, choice_ind)
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
    def get_all_statements(player_index: int) -> tuple[Statement, ...]:
        """Required for all player types. Returns all possible role statements."""
        statements: tuple[Statement, ...] = ()
        for k in range(const.NUM_CENTER):
            statements += Drunk.get_drunk_statements(
                player_index, const.NUM_PLAYERS + k
            )
        return statements

    def json_repr(self) -> dict[str, Any]:
        """Gets JSON representation of a Drunk player."""
        return super().json_repr() | {"choice_ind": self.choice_ind}
