""" seer.py """
from __future__ import annotations

import random
from typing import Any, Dict, List, Optional, Tuple

from src import const, util
from src.const import logger
from src.statements import Statement

from ..player import Player


class Seer(Player):
    """ Seer Player class. """

    def __init__(
        self,
        player_index: int,
        choice_1: Tuple[int, str],
        choice_2: Tuple[Optional[int], Optional[str]] = (None, None),
    ):
        super().__init__(player_index)
        self.choice_1 = tuple(choice_1)
        self.choice_2 = tuple(choice_2)
        self.statements += self.get_seer_statements(player_index, choice_1, choice_2)

    @classmethod
    def awake_init(
        cls, player_index: int, game_roles: List[str], original_roles: List[str]
    ) -> Seer:
        """ Initializes Seer - either sees 2 center cards or 1 player card. """
        del original_roles

        # Pick two center cards more often, because that generally yields higher win rates.
        prob = const.CENTER_SEER_PROB
        is_user = const.IS_USER[player_index]
        choose_center = random.choices([True, False], [prob, 1 - prob])[0]
        if choose_center and const.NUM_CENTER > 1:
            peek_ind1 = util.get_center(is_user)
            peek_ind2 = util.get_center(is_user, (peek_ind1,))
            peek_char1 = game_roles[peek_ind1]
            peek_char2 = game_roles[peek_ind2]
            logger.debug(
                f"[Hidden] Seer sees that Center {peek_ind1 - const.NUM_PLAYERS} is a "
                f"{peek_char1}, Center {peek_ind2 - const.NUM_PLAYERS} is a {peek_char2}."
            )
            if is_user:
                logger.info(
                    f"You see that Center {peek_ind1 - const.NUM_PLAYERS} is a {peek_char1}, "
                    f"and Center {peek_ind2 - const.NUM_PLAYERS} is a {peek_char2}."
                )
            return cls(player_index, (peek_ind1, peek_char1), (peek_ind2, peek_char2))

        peek_ind = util.get_player(is_user, (player_index,))
        peek_char = game_roles[peek_ind]
        logger.debug(f"[Hidden] Seer sees that Player {peek_ind} is a {peek_char}.")
        if is_user:
            logger.info(f"You see that Player {peek_ind} is a {peek_char}.")
        return cls(player_index, (peek_ind, peek_char))

    @staticmethod
    def get_seer_statements(
        player_index: int,
        choice_1: Tuple[int, str],
        choice_2: Tuple[Optional[int], Optional[str]] = (None, None),
    ) -> List[Statement]:
        """ Gets Seer Statement. """
        seen_index, seen_role = choice_1
        seen_index2, seen_role2 = choice_2
        sentence = f"I am a Seer and I saw that Player {seen_index} was a {seen_role}."
        knowledge = [(player_index, {"Seer"}), (seen_index, {seen_role})]
        if seen_index2 is not None and seen_role2 is not None:
            sentence = (
                f"I am a Seer and I saw that Center {seen_index - const.NUM_PLAYERS} was a"
                f" {seen_role} and that Center {seen_index2 - const.NUM_PLAYERS}"
                f" was a {seen_role2}."
            )
            knowledge.append((seen_index2, {seen_role2}))
        return [Statement(sentence, knowledge)]

    @staticmethod
    def get_all_statements(player_index: int) -> List[Statement]:
        """ Required for all player types. Returns all possible role statements. """
        statements: List[Statement] = []
        for role in const.SORTED_ROLE_SET:
            for i in range(const.NUM_PLAYERS):  # OK: 'Hey, I'm a Seer and I saw another Seer...'
                statements += Seer.get_seer_statements(player_index, (i, role))
        # Wolf using these usually gives themselves away
        role_set = list(const.SORTED_ROLE_SET)
        role_set.remove("Seer")
        for cent1 in range(const.NUM_CENTER):
            for cent2 in range(cent1 + 1, const.NUM_CENTER):
                for role1 in role_set:
                    for role2 in role_set:
                        if role1 != role2 or const.ROLE_COUNTS[role1] >= 2:
                            choice_1 = (cent1 + const.NUM_PLAYERS, role1)
                            choice_2 = (cent2 + const.NUM_PLAYERS, role2)
                            statements += Seer.get_seer_statements(player_index, choice_1, choice_2)
        return statements

    def json_repr(self) -> Dict[str, Any]:
        """ Gets JSON representation of a Seer player. """
        return {
            "type": self.role,
            "player_index": self.player_index,
            "choice_1": self.choice_1,
            "choice_2": self.choice_2,
        }
