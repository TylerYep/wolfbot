""" random_wolf.py """
import random
from typing import Any, Tuple

from src import const, roles
from src.statements import Statement


def get_wolf_statements_random(player_obj: Any) -> Tuple[Statement, ...]:
    """ Gets Random Wolf statements. """
    statements: Tuple[Statement, ...] = ()
    village_roles = sorted(tuple(const.VILLAGE_ROLES))
    random.shuffle(village_roles)
    for role in village_roles:
        role_obj = roles.get_role_obj(role)
        statements += role_obj.get_all_statements(player_obj.player_index)
    return statements
