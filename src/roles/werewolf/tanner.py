""" tanner.py """
from __future__ import annotations

import random
from typing import Any, Dict, List, Tuple

from src import const
from src.algorithms import switching_solver as solver
from src.predictions import make_unrestricted_prediction
from src.statements import Statement

from ..player import Player
from .wolf_variants import get_statement_expectimax, get_wolf_statements_random


class Tanner(Player):
    """ Tanner Player class. """

    def __init__(self, player_index: int):
        super().__init__(player_index)
        self.statements = get_wolf_statements_random(self)

    @classmethod
    def awake_init(
        cls, player_index: int, game_roles: List[str], original_roles: List[str]
    ) -> Tanner:
        """ Initializes Tanner when night falls. """
        del game_roles, original_roles
        return cls(player_index)

    def get_statement(self, stated_roles: List[str], previous: List[Statement]) -> Statement:
        """ Get Tanner Statement. """
        if const.EXPECTIMAX_TANNER:
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
        return val

    def json_repr(self) -> Dict[str, Any]:
        """ Gets JSON representation of a Tanner player. """
        return {"type": self.role, "player_index": self.player_index}
