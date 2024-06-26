from __future__ import annotations

import random
from typing import TYPE_CHECKING, Self, override

from wolfbot import const
from wolfbot.enums import Role, lru_cache
from wolfbot.predictions import make_unrestricted_prediction
from wolfbot.roles.player import Player
from wolfbot.roles.werewolf.wolf_variants import (
    get_statement_expectimax,
    get_wolf_statements_random,
)
from wolfbot.solvers import switching_solver as solver

if TYPE_CHECKING:
    from wolfbot.statements import KnowledgeBase, Statement


class Tanner(Player):
    """Tanner Player class."""

    @classmethod
    @override
    def awake_init(cls, player_index: int, game_roles: list[Role]) -> Self:
        """Initializes Tanner when night falls."""
        del game_roles
        return cls(player_index)

    @staticmethod
    @lru_cache
    @override
    def get_all_statements(player_index: int) -> tuple[Statement, ...]:
        """Required for all player types. Returns all possible role statements."""
        raise NotImplementedError

    @override
    def analyze(self, knowledge_base: KnowledgeBase) -> None:
        """Updates Player state given new information."""
        super().analyze(knowledge_base)
        self.statements += get_wolf_statements_random(self.player_index)

    @override
    def get_statement(self, knowledge_base: KnowledgeBase) -> Statement:
        """Get Tanner Statement."""
        if const.EXPECTIMAX_TANNER:
            return get_statement_expectimax(self, knowledge_base)
        return super().get_statement(knowledge_base)

    def eval_fn(self, statement_list: tuple[Statement]) -> int:
        """
        Evaluates a complete or incomplete game.
        """
        solver_result = random.choice(solver(statement_list))
        predictions = make_unrestricted_prediction(solver_result)
        val = 10
        if not predictions:
            return -10
        if predictions[self.player_index] is Role.WOLF:
            val += 10
        return val
