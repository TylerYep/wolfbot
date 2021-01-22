""" minion.py """
from __future__ import annotations

import random
from typing import Any

from src import const, util
from src.const import Role, logger, lru_cache
from src.predictions import make_unrestricted_prediction
from src.roles.player import Player
from src.roles.werewolf.wolf_variants import (
    get_statement_expectimax,
    get_wolf_statements,
    get_wolf_statements_random,
)
from src.solvers import switching_solver as solver
from src.statements import KnowledgeBase, Statement


class Minion(Player):
    """ Minion Player class. """

    def __init__(self, player_index: int, wolf_indices: tuple[int, ...]):
        super().__init__(player_index)
        self.wolf_indices = wolf_indices

    @classmethod
    def awake_init(
        cls, player_index: int, game_roles: list[Role], original_roles: tuple[Role, ...]
    ) -> Minion:
        """ Initializes Minion - gets Wolf indices. """
        del game_roles
        is_user = const.IS_USER[player_index]
        wolf_indices = util.find_all_player_indices(original_roles, Role.WOLF)
        logger.debug(f"[Hidden] Wolves are at indices: {list(wolf_indices)}")
        if is_user:
            logger.info(f"Wolves are at indices: {list(wolf_indices)}", cache=True)
        return cls(player_index, wolf_indices)

    @staticmethod
    @lru_cache
    def get_all_statements(player_index: int) -> tuple[Statement, ...]:
        """ Required for all player types. Returns all possible role statements. """
        raise NotImplementedError

    def analyze(self, knowledge_base: KnowledgeBase) -> None:
        """ Updates Player state given new information. """
        super().analyze(knowledge_base)
        if const.USE_REG_WOLF:
            self.statements += get_wolf_statements(self, knowledge_base)
        else:
            self.statements += get_wolf_statements_random(self.player_index)

    def get_statement(self, knowledge_base: KnowledgeBase) -> Statement:
        """ Get Minion Statement. """
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

    def json_repr(self) -> dict[str, Any]:
        """ Gets JSON representation of a Minion player. """
        return super().json_repr() | {"wolf_indices": self.wolf_indices}
