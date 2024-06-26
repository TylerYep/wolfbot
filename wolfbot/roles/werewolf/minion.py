from __future__ import annotations

import random
from typing import TYPE_CHECKING, Any, Self, override

from wolfbot import const
from wolfbot.enums import Role, lru_cache
from wolfbot.game_utils import find_all_player_indices
from wolfbot.log import logger
from wolfbot.predictions import make_unrestricted_prediction
from wolfbot.roles.player import Player
from wolfbot.roles.werewolf.wolf_variants import (
    get_statement_expectimax,
    get_wolf_statements,
    get_wolf_statements_random,
)
from wolfbot.solvers import switching_solver as solver

if TYPE_CHECKING:
    from wolfbot.statements import KnowledgeBase, Statement


class Minion(Player):
    """Minion Player class."""

    def __init__(self, player_index: int, wolf_indices: tuple[int, ...]) -> None:
        super().__init__(player_index)
        self.wolf_indices = wolf_indices

    @classmethod
    @override
    def awake_init(cls, player_index: int, game_roles: list[Role]) -> Self:
        """Initializes Minion - gets Wolf indices."""
        is_user = const.IS_USER[player_index]
        wolf_indices = find_all_player_indices(game_roles, Role.WOLF)
        logger.debug(f"[Hidden] Wolves are at indices: {list(wolf_indices)}")
        if is_user:
            logger.info(f"Wolves are at indices: {list(wolf_indices)}", cache=True)
        return cls(player_index, wolf_indices)

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
        if const.USE_REG_WOLF:
            self.statements += get_wolf_statements(self, knowledge_base)
        else:
            self.statements += get_wolf_statements_random(self.player_index)

    @override
    def get_statement(self, knowledge_base: KnowledgeBase) -> Statement:
        """Get Minion Statement."""
        if const.EXPECTIMAX_MINION:
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
        for wolfi in self.wolf_indices:
            if predictions[wolfi] is Role.WOLF:
                val -= 7
            if Role.WOLF in solver_result.possible_roles[wolfi]:
                val -= 5
        return val

    @override
    def json_repr(self) -> dict[str, Any]:
        """Gets JSON representation of a Minion player."""
        return super().json_repr() | {"wolf_indices": self.wolf_indices}
