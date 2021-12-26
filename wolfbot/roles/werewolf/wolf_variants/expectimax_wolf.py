import random
from typing import Any

from wolfbot import const, roles
from wolfbot.algorithms import expectimax
from wolfbot.enums import lru_cache
from wolfbot.log import logger
from wolfbot.solvers import switching_solver as solver
from wolfbot.statements import KnowledgeBase, Statement


@lru_cache
def get_expected_statements() -> dict[int, tuple[Statement, ...]]:
    """
    Gets all possible statements that can be made by a Village player from any index.
    Used to find the 'expect' part of the Expectimax algorithm.
    Returns set of statement objects.
    """
    possible: dict[int, tuple[Statement, ...]] = {}
    for player_index in range(const.NUM_PLAYERS):
        statements: tuple[Any, ...] = ()
        for role in sorted(const.VILLAGE_ROLES):
            role_obj = roles.get_role_obj(role)
            statements += role_obj.get_all_statements(player_index)
        possible[player_index] = statements
    return possible


def get_statement_expectimax(
    player_obj: Any, knowledge_base: KnowledgeBase
) -> Statement:
    """Gets Expectimax Wolf statement."""
    prev_statements = tuple(knowledge_base.final_claims)
    expected_statements = get_expected_statements()
    player_obj.statements = [
        x for x in player_obj.statements if x.priority > player_obj.prev_priority
    ]

    # Initialize start_state to use all previous statements
    start_state = random.choice(solver(prev_statements))
    best_val, best_move = expectimax(
        player_obj,
        expected_statements,
        prev_statements,
        start_state,
        player_obj.player_index,
    )
    logger.debug(f"[Hidden] Evaluation Function Score: {best_val}")
    if best_move is None:
        raise RuntimeError("best_move should not be None.")
    return best_move
