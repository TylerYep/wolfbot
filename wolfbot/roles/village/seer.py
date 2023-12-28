from __future__ import annotations

from typing import Any, Self, override

from wolfbot import const
from wolfbot.enums import Role, lru_cache
from wolfbot.game_utils import get_center, get_numeric_input, get_player
from wolfbot.log import logger
from wolfbot.roles.player import Player
from wolfbot.statements import Statement
from wolfbot.util import weighted_coin_flip


class Seer(Player):
    """Seer Player class."""

    def __init__(
        self,
        player_index: int,
        choice_1: tuple[int, Role],
        choice_2: tuple[int | None, Role | None] = (None, None),
    ) -> None:
        super().__init__(player_index)
        self.choice_1, self.choice_2 = choice_1, choice_2
        self.statements += self.get_seer_statements(player_index, choice_1, choice_2)

    @classmethod
    @override
    def awake_init(cls, player_index: int, game_roles: list[Role]) -> Self:
        """Initializes Seer - either sees 2 center cards or 1 player card."""
        is_user = const.IS_USER[player_index]
        if const.NUM_CENTER > 1:
            if is_user:
                logger.info("Do you want to see 1 player card or 2 center cards?")
                choose_center = bool(get_numeric_input(1, 3) - 1)
            else:
                # Pick two center cards more often, because
                # that generally yields higher win rates.
                choose_center = weighted_coin_flip(const.CENTER_SEER_PROB)

            if choose_center:
                peek_ind1 = get_center(is_user)
                peek_ind2 = get_center(is_user, (peek_ind1,))
                peek_char1 = game_roles[peek_ind1]
                peek_char2 = game_roles[peek_ind2]
                logger.debug(
                    f"[Hidden] Seer sees that Center {peek_ind1 - const.NUM_PLAYERS} "
                    f"is a {peek_char1}, Center {peek_ind2 - const.NUM_PLAYERS} "
                    f"is a {peek_char2}."
                )
                if is_user:
                    logger.info(
                        f"You see that Center {peek_ind1 - const.NUM_PLAYERS} "
                        f"is a {peek_char1}, and "
                        f"Center {peek_ind2 - const.NUM_PLAYERS} is a {peek_char2}.",
                        cache=True,
                    )
                return cls(
                    player_index, (peek_ind1, peek_char1), (peek_ind2, peek_char2)
                )

        peek_ind = get_player(is_user, (player_index,))
        peek_char = game_roles[peek_ind]
        logger.debug(f"[Hidden] Seer sees that Player {peek_ind} is a {peek_char}.")
        if is_user:
            logger.info(f"You see that Player {peek_ind} is a {peek_char}.", cache=True)
        return cls(player_index, (peek_ind, peek_char))

    @staticmethod
    @lru_cache
    def get_seer_statements(
        player_index: int,
        choice_1: tuple[int, Role],
        choice_2: tuple[int | None, Role | None] = (None, None),
    ) -> tuple[Statement, ...]:
        """Gets Seer Statement."""
        seen_index, seen_role = choice_1
        seen_index2, seen_role2 = choice_2
        sentence = f"I am a Seer and I saw that Player {seen_index} was a {seen_role}."
        knowledge = [
            (player_index, frozenset({Role.SEER})),
            (seen_index, frozenset({seen_role})),
        ]
        if seen_index2 is not None and seen_role2 is not None:
            sentence = (
                f"I am a Seer and I saw that Center {seen_index - const.NUM_PLAYERS} "
                f"was a {seen_role} and that Center {seen_index2 - const.NUM_PLAYERS} "
                f"was a {seen_role2}."
            )
            knowledge.append((seen_index2, frozenset({seen_role2})))
        return (Statement(sentence, tuple(knowledge)),)

    @staticmethod
    @lru_cache
    @override
    def get_all_statements(player_index: int) -> tuple[Statement, ...]:
        """Required for all player types. Returns all possible role statements."""
        statements: tuple[Statement, ...] = ()
        for role in const.SORTED_ROLE_SET:
            for i in range(
                const.NUM_PLAYERS
            ):  # OK: 'Hey, I'm a Seer and I saw another Seer...'
                statements += Seer.get_seer_statements(player_index, (i, role))
        # Wolf using these usually gives themselves away
        role_set = list(const.SORTED_ROLE_SET)
        role_set.remove(Role.SEER)
        for cent1 in range(const.NUM_CENTER):
            for cent2 in range(cent1 + 1, const.NUM_CENTER):
                for role1 in role_set:
                    for role2 in role_set:
                        if role1 != role2 or const.ROLE_COUNTS[role1] >= 2:
                            choice_1 = (cent1 + const.NUM_PLAYERS, role1)
                            choice_2 = (cent2 + const.NUM_PLAYERS, role2)
                            statements += Seer.get_seer_statements(
                                player_index, choice_1, choice_2
                            )
        return statements

    @override
    def json_repr(self) -> dict[str, Any]:
        """Gets JSON representation of a Seer player."""
        return super().json_repr() | {
            "choice_1": self.choice_1,
            "choice_2": self.choice_2,
        }
