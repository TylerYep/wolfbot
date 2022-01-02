from __future__ import annotations

from typing import Any

from wolfbot import const
from wolfbot.enums import Role, SwitchPriority, lru_cache
from wolfbot.game_utils import GameRoles, get_player
from wolfbot.log import logger
from wolfbot.roles.player import Player
from wolfbot.statements import Statement


class Robber(Player):
    """Robber Player class."""

    def __init__(self, player_index: int, choice_ind: int, new_role: Role):
        super().__init__(player_index)
        self.choice_ind = choice_ind
        self.new_role = new_role
        self.statements += self.get_robber_statements(
            player_index, choice_ind, new_role
        )

    @classmethod
    def awake_init(cls, player_index: int, game_roles: GameRoles) -> Robber:
        """Initializes Robber - switches roles with another player."""
        is_user = const.IS_USER[player_index]
        choice_ind = get_player(is_user, (player_index,))
        choice_char = game_roles[choice_ind]
        logger.debug(
            f"[Hidden] Robber switches with Player {choice_ind} "
            f"and becomes a {choice_char}."
        )
        if is_user:
            logger.info(
                f"You switched with Player {choice_ind} and are now a {choice_char}!",
                cache=True,
            )
        game_roles.swap_characters(player_index, choice_ind)
        return cls(player_index, choice_ind, choice_char)

    @staticmethod
    @lru_cache
    def get_robber_statements(
        player_index: int, choice_ind: int, choice_char: Role
    ) -> tuple[Statement, ...]:
        """Gets Robber Statement."""
        sentence = (
            f"I am a Robber and I swapped with Player {choice_ind}. "
            f"I am now a {choice_char}."
        )
        knowledge = (
            (player_index, frozenset({Role.ROBBER})),
            (choice_ind, frozenset({choice_char})),
        )
        switches = ((SwitchPriority.ROBBER, player_index, choice_ind),)
        return (Statement(sentence, knowledge, switches),)

    @staticmethod
    @lru_cache
    def get_all_statements(player_index: int) -> tuple[Statement, ...]:
        """Required for all player types. Returns all possible role statements."""
        statements: tuple[Statement, ...] = ()
        for i in range(const.NUM_PLAYERS):
            for role in const.SORTED_ROLE_SET:
                if (
                    player_index != i
                ):  # OK: 'I robbed Player 0 and now I'm a Wolf... ;)'
                    statements += Robber.get_robber_statements(player_index, i, role)
        return statements

    def json_repr(self) -> dict[str, Any]:
        """Gets JSON representation of a Robber player."""
        return super().json_repr() | {
            "choice_ind": self.choice_ind,
            "new_role": self.new_role,
        }
