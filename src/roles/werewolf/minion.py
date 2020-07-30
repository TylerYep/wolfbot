""" minion.py """
from __future__ import annotations

import random
from typing import Any, Dict, List, Tuple

from src import const, util
from src.const import logger, lru_cache
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

    def __init__(self, player_index: int, wolf_indices: Tuple[int, ...]):
        super().__init__(player_index)
        self.wolf_indices = wolf_indices

    @classmethod
    def awake_init(
        cls, player_index: int, game_roles: List[str], original_roles: Tuple[str, ...]
    ) -> Minion:
        """ Initializes Minion - gets Wolf indices. """
        del game_roles
        is_user = const.IS_USER[player_index]
        wolf_indices = util.find_all_player_indices(original_roles, "Wolf")
        logger.debug(f"[Hidden] Wolves are at indices: {list(wolf_indices)}")
        if is_user:
            logger.info(f"Wolves are at indices: {list(wolf_indices)}", cache=True)
        return cls(player_index, wolf_indices)

    @staticmethod
    @lru_cache
    def get_all_statements(player_index: int) -> Tuple[Statement, ...]:
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
