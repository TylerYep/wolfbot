from __future__ import annotations

from typing import Any, Self, override

from wolfbot import const
from wolfbot.enums import Role, lru_cache
from wolfbot.game_utils import get_player
from wolfbot.log import logger
from wolfbot.roles.player import Player
from wolfbot.statements import Statement


class Doppelganger(Player):
    """Doppelganger Player class."""

    def __init__(self, player_index: int, choice_ind: int, new_role: Role) -> None:
        super().__init__(player_index)
        self.choice_ind = choice_ind
        self.new_role = new_role
        self.statements += self.get_doppelganger_statements(player_index, new_role)

    @classmethod
    @override
    def awake_init(cls, player_index: int, game_roles: list[Role]) -> Self:
        """Initializes Doppelganger - learns new role."""
        from wolfbot.roles import get_role_obj

        is_user = const.IS_USER[player_index]
        choice_ind = get_player(is_user, (player_index,))
        choice_char = game_roles[choice_ind]
        logger.debug(
            f"[Hidden] Doppelganger copies Player {choice_ind} "
            f"and becomes a {choice_char}."
        )
        if is_user:
            logger.info(
                f"You copied Player {choice_ind} and are now a {choice_char}!",
                cache=True,
            )
        # Temporarily set Doppelganger in game_roles to the new role
        # so she wakes up with the other characters.
        game_roles[player_index] = choice_char
        if choice_char in (Role.WOLF, Role.MASON):
            get_role_obj(choice_char).awake_init(player_index, game_roles)

        # else do switches later
        return cls(player_index, choice_ind, choice_char)

    @staticmethod
    @lru_cache
    def get_doppelganger_statements(
        player_index: int, new_role: Role
    ) -> tuple[Statement, ...]:
        """Gets Doppelganger Statement."""
        knowledge = ((player_index, frozenset({Role.DOPPELGANGER})),)
        sentence = f"I am a Doppelganger and when I woke up I was a {new_role}."
        return (Statement(sentence, knowledge),)

    @staticmethod
    @lru_cache
    @override
    def get_all_statements(player_index: int) -> tuple[Statement, ...]:
        """Required for all player types. Returns all possible role statements."""
        statements: list[Statement] = []
        for role in const.SORTED_ROLE_SET:
            statements += Doppelganger.get_doppelganger_statements(player_index, role)
        return tuple(statements)

    @override
    def json_repr(self) -> dict[str, Any]:
        """Gets JSON representation of an Doppelganger player."""
        return super().json_repr() | {"new_role": self.new_role}
