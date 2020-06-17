""" expectimax_wolf.py """
import random
from typing import Any, Dict, List

from src import const, roles
from src.algorithms import expectimax
from src.statements import Statement


def get_expected_statements() -> Dict[int, List[Statement]]:
    """
    Gets all possible statements that can be made by a Village player from any index.
    Used to find the 'expect' part of the Expectimax algorithm.
    Returns set of statement objects.
    """
    possible: Dict[int, List[Statement]] = {}
    for player_index in range(const.NUM_PLAYERS):
        statements = []
        village_roles = sorted(tuple(const.VILLAGE_ROLES))
        random.shuffle(village_roles)
        for role in village_roles:
            role_obj = roles.get_role_obj(role)
            statements += role_obj.get_all_statements(player_index)
        possible[player_index] = statements
    return possible


def get_statement_expectimax(player_obj: Any, prev_statements: List[Statement]) -> Statement:
    """ Gets Expectimax Wolf statement. """
    expected_player_statements = get_expected_statements()
    player_obj.statements = [
        x for x in player_obj.statements if x.priority > player_obj.prev_priority
    ]
    next_statement = expectimax(player_obj, tuple(prev_statements), expected_player_statements)
    player_obj.prev_priority = next_statement.priority
    return next_statement
