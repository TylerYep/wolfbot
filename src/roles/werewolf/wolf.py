""" wolf.py """
from __future__ import annotations

import random
from typing import Any, Dict, List, Optional, Tuple

from overrides import overrides

from src import const, util
from src.const import logger
from src.predictions import make_unrestricted_prediction
from src.roles.player import Player
from src.roles.werewolf.wolf_variants import (
    get_center_wolf_statements,
    get_statement_expectimax,
    get_statement_rl,
    get_wolf_statements,
    get_wolf_statements_random,
)
from src.solvers import switching_solver as solver
from src.statements import KnowledgeBase, Statement


class Wolf(Player):
    """ Wolf Player class. """

    def __init__(
        self,
        player_index: int,
        wolf_indices: List[int],
        center_index: Optional[int] = None,
        center_role: Optional[str] = None,
    ):
        super().__init__(player_index)
        self.wolf_indices = wolf_indices
        self.center_index = center_index
        self.center_role = center_role

    @classmethod
    @overrides
    def awake_init(
        cls, player_index: int, game_roles: List[str], original_roles: List[str]
    ) -> Wolf:
        """
        Constructor: original_roles defaults to [] when a player becomes a Wolf and realizes it.
        Initializes Wolf - gets Wolf indices and a random center card, if applicable.
        """
        is_user = const.IS_USER[player_index]
        center_index, center_role = None, None
        wolf_indices = util.find_all_player_indices(original_roles, "Wolf")
        if len(wolf_indices) == 1 and const.NUM_CENTER > 0:
            center_index = util.get_center(is_user)
            center_role = game_roles[center_index]
            if is_user:
                logger.info(
                    f"You see Center {center_index - const.NUM_PLAYERS} is a {center_role}.",
                    cache=True,
                )
        logger.debug(f"[Hidden] Wolves are at indices: {wolf_indices}")
        if is_user:
            logger.info(f"Wolves are at indices: {wolf_indices}", cache=True)

        return cls(player_index, wolf_indices, center_index, center_role)

    @staticmethod
    @overrides
    def get_all_statements(player_index: int) -> Tuple[Statement, ...]:
        """ Required for all player types. Returns all possible role statements. """
        raise NotImplementedError

    @overrides
    def analyze(self, knowledge_base: KnowledgeBase) -> None:
        """ Updates Player state given new information. """
        super().analyze(knowledge_base)
        if const.USE_REG_WOLF:
            if self.center_role not in (None, "Wolf", "Mason"):
                center_statements = get_center_wolf_statements(self, knowledge_base)
                self.statements += (
                    center_statements
                    if center_statements
                    else get_wolf_statements(self, knowledge_base)
                )
            else:
                self.statements += get_wolf_statements(self, knowledge_base)
        else:
            self.statements += get_wolf_statements_random(self.player_index)

    @overrides
    def get_statement(self, knowledge_base: KnowledgeBase) -> Statement:
        """ Get Wolf Statement. """
        if const.USE_RL_WOLF:
            # Choose one statement to return by default
            default_statement = super().get_statement(knowledge_base)
            return get_statement_rl(self, knowledge_base, default_statement)

        if const.EXPECTIMAX_WOLF:
            return get_statement_expectimax(self, knowledge_base)

        return super().get_statement(knowledge_base)

    def eval_fn(self, statement_list: Tuple[Statement]) -> int:
        """
        Evaluates a complete or incomplete game.
        # wolves in a positions - # of ones that are actually wolves, size of set
        """
        solver_result = random.choice(solver(statement_list))
        predictions = make_unrestricted_prediction(solver_result)
        val = 10
        if not predictions:
            return -10
        for wolfi in self.wolf_indices:
            if predictions[wolfi] == "Wolf":
                val -= 7
            if "Wolf" in solver_result.possible_roles[wolfi]:
                val -= 5
        return val

    @overrides
    def json_repr(self) -> Dict[str, Any]:
        """ Gets JSON representation of a Wolf player. """
        json_dict = super().json_repr()
        json_dict.update(
            {
                "wolf_indices": self.wolf_indices,
                "center_index": self.center_index,
                "center_role": self.center_role,
            }
        )
        return json_dict
