""" tanner.py """
from __future__ import annotations

import random
from typing import List, Tuple

from overrides import overrides

from src import const
from src.predictions import make_unrestricted_prediction
from src.roles.player import Player
from src.roles.werewolf.wolf_variants import get_statement_expectimax, get_wolf_statements_random
from src.solvers import switching_solver as solver
from src.statements import KnowledgeBase, Statement


class Tanner(Player):
    """ Tanner Player class. """

    def __init__(self, player_index: int):
        super().__init__(player_index)
        self.statements = get_wolf_statements_random(self.player_index)

    @classmethod
    @overrides
    def awake_init(
        cls, player_index: int, game_roles: List[str], original_roles: List[str]
    ) -> Tanner:
        """ Initializes Tanner when night falls. """
        del game_roles, original_roles
        return cls(player_index)

    @staticmethod
    @overrides
    def get_all_statements(player_index: int) -> Tuple[Statement, ...]:
        """ Required for all player types. Returns all possible role statements. """
        raise NotImplementedError

    @overrides
    def get_statement(self, knowledge_base: KnowledgeBase) -> Statement:
        """ Get Tanner Statement. """
        if const.EXPECTIMAX_TANNER:
            return get_statement_expectimax(self, knowledge_base)
        return super().get_statement(knowledge_base)

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
