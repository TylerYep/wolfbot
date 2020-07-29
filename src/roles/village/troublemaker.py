""" troublemaker.py """
from __future__ import annotations

from typing import Any, Dict, List, Tuple

from overrides import overrides

from src import const, util
from src.const import SwitchPriority, logger, lru_cache
from src.roles.player import Player
from src.statements import Statement


class Troublemaker(Player):
    """ Troublemaker Player class. """

    def __init__(self, player_index: int, choice_ind1: int, choice_ind2: int):
        super().__init__(player_index)
        self.choice_ind1, self.choice_ind2 = choice_ind1, choice_ind2
        self.statements += self.get_troublemaker_statements(player_index, choice_ind1, choice_ind2)

    @classmethod
    @overrides
    def awake_init(
        cls, player_index: int, game_roles: List[str], original_roles: Tuple[str, ...]
    ) -> Troublemaker:
        """ Initializes Troublemaker - switches one player with another player. """
        del original_roles
        assert const.NUM_PLAYERS > 2
        is_user = const.IS_USER[player_index]
        if is_user:
            logger.info("Choose two players to switch places:")
        choice_1 = util.get_player(is_user, (player_index,))
        choice_2 = util.get_player(is_user, (player_index, choice_1))

        util.swap_characters(game_roles, choice_1, choice_2)
        logger.debug(f"[Hidden] Troublemaker switches Player {choice_1} and Player {choice_2}.")
        if is_user:
            logger.info(f"You switch Player {choice_1} with Player {choice_2}.", cache=True)

        return cls(player_index, choice_1, choice_2)

    @staticmethod
    @lru_cache
    def get_troublemaker_statements(
        player_index: int, tmkr_ind1: int, tmkr_ind2: int
    ) -> Tuple[Statement, ...]:
        """ Gets Troublemaker Statement. """
        sentence = f"I am a Troublemaker and I swapped Player {tmkr_ind1} and Player {tmkr_ind2}."
        knowledge = ((player_index, frozenset({"Troublemaker"})),)
        switches = ((SwitchPriority.TROUBLEMAKER, tmkr_ind1, tmkr_ind2),)
        return (Statement(sentence, knowledge, switches),)

    @staticmethod
    @lru_cache
    @overrides
    def get_all_statements(player_index: int) -> Tuple[Statement, ...]:
        """ Required for all player types. Returns all possible role statements. """
        statements: Tuple[Statement, ...] = ()
        for i in range(const.NUM_PLAYERS):
            for j in range(i + 1, const.NUM_PLAYERS):
                # Troublemaker should not refer to themselves; ensure all three values are unique
                if len({i, j, player_index}) == 3:
                    statements += Troublemaker.get_troublemaker_statements(player_index, i, j)
        return statements

    @overrides
    def json_repr(self) -> Dict[str, Any]:
        """ Gets JSON representation of a Troublemaker player. """
        json_dict = super().json_repr()
        json_dict.update({"choice_ind1": self.choice_ind1, "choice_ind2": self.choice_ind2})
        return json_dict
