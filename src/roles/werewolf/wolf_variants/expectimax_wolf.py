""" expectimax_wolf.py """
import random
from typing import Any, Dict, Tuple

from src import const, roles
from src.algorithms import expectimax
from src.const import logger
from src.solvers import switching_solver as solver
from src.statements import KnowledgeBase, Statement


def get_expected_statements() -> Dict[int, Tuple[Statement, ...]]:
    """
    Gets all possible statements that can be made by a Village player from any index.
    Used to find the 'expect' part of the Expectimax algorithm.
    Returns set of statement objects.
    """
    possible: Dict[int, Tuple[Statement, ...]] = {}
    for player_index in range(const.NUM_PLAYERS):
        statements = ()
        village_roles = sorted(tuple(const.VILLAGE_ROLES))
        random.shuffle(village_roles)
        for role in village_roles:
            role_obj = roles.get_role_obj(role)
            statements += role_obj.get_all_statements(player_index)
        possible[player_index] = statements
    return possible


def get_statement_expectimax(player_obj: Any, knowledge_base: KnowledgeBase) -> Statement:
    """ Gets Expectimax Wolf statement. """
    prev_statements = tuple(knowledge_base.final_claims)
    expected_statements = get_expected_statements()
    player_obj.statements = [
        x for x in player_obj.statements if x.priority > player_obj.prev_priority
    ]

    # Initialize start_state to use all previous statements
    start_state = random.choice(solver(prev_statements))
    best_val, best_move = expectimax(
        player_obj, expected_statements, prev_statements, start_state, player_obj.player_index
    )
    logger.debug(f"[Hidden] Evaluation Function Score: {best_val}")
    assert best_move is not None
    return best_move
