''' random_wolf.py '''
from typing import Any, List
import random

from src.statements import Statement
from src import const, roles


def get_wolf_statements_random(player_obj: Any) -> List[Statement]:
    ''' Gets Random Wolf statements. '''
    statements: List[Statement] = []
    village_roles = sorted(tuple(const.VILLAGE_ROLES))
    random.shuffle(village_roles)
    for role in village_roles:
        role_obj = roles.get_role_obj(role)
        statements += role_obj.get_all_statements(player_obj.player_index)
    return statements
