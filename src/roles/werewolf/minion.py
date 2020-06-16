""" minion.py """
from __future__ import annotations

import random
from typing import Any, Dict, List, Tuple

from src import const, util
from src.algorithms import switching_solver as solver
from src.const import logger
from src.predictions import make_unrestricted_prediction
from src.statements import Statement

from ..player import Player
from .wolf_variants import get_statement_expectimax, get_wolf_statements, get_wolf_statements_random


class Minion(Player):
    """ Minion Player class. """

    def __init__(self, player_index: int, wolf_indices: List[int]):
        super().__init__(player_index)
        self.wolf_indices = wolf_indices

    @classmethod
    def awake_init(
        cls, player_index: int, game_roles: List[str], original_roles: List[str]
    ) -> Minion:
        """ Initializes Minion - gets Wolf indices. """
        del game_roles
        is_user = const.IS_USER[player_index]
        wolf_indices: List[int] = []
        if original_roles:
            wolf_indices = util.find_all_player_indices(original_roles, "Wolf")
            logger.debug(f"[Hidden] Wolves are at indices: {wolf_indices}")
            if is_user:
                logger.info(f"Wolves are at indices: {wolf_indices}", cache=True)
        return cls(player_index, wolf_indices)

    def get_statement(self, stated_roles: List[str], previous: List[Statement]) -> Statement:
        """ Get Minion Statement. """
        if const.USE_REG_WOLF:
            self.statements += get_wolf_statements(self, stated_roles, previous)
        else:
            self.statements += get_wolf_statements_random(self)

        if const.EXPECTIMAX_MINION:
            return get_statement_expectimax(self, previous)

        return super().get_statement(stated_roles, previous)

    def eval_fn(self, statement_list: Tuple[Statement]) -> int:
        """
        Evaluates a complete or incomplete game.
        """
        solver_result = random.choice(solver(statement_list))
        predictions = make_unrestricted_prediction(solver_result)
        val = 10
        if not predictions:
            return -10
        if predictions[self.player_index] == "Wolf":
            val += 10
        for wolfi in self.wolf_indices:
            if predictions[wolfi] == "Wolf":
                val -= 7
            if "Wolf" in solver_result.possible_roles[wolfi]:
                val -= 5
        return val

    def json_repr(self) -> Dict[str, Any]:
        """ Gets JSON representation of a Minion player. """
        json_dict = super().json_repr()
        json_dict.update({"wolf_indices": self.wolf_indices})
        return json_dict
