""" random_wolf.py """
import random
from typing import Tuple

from src import const, roles
from src.statements import Statement


def get_wolf_statements_random(player_index: int) -> Tuple[Statement, ...]:
    """
    Gets Random Wolf statements.
    Empirically, adding an lru_cache to this function seems to slow the program down,
    possibly because this re-caches get_all_statement calls unnecessarily.
    """
    statements: Tuple[Statement, ...] = ()
    village_roles = sorted(tuple(const.VILLAGE_ROLES))
    random.shuffle(village_roles)
    for role in village_roles:
        role_obj = roles.get_role_obj(role)
        statements += role_obj.get_all_statements(player_index)
    return statements
