''' random_wolf.py '''
from typing import Any, List

from src.statements import Statement
from src import const, roles

def get_wolf_statements_random(player_obj: Any) -> List[Statement]:
    ''' Gets Random Wolf Player statement. '''
    statements = []
    for role in const.VILLAGE_ROLES:
        role_obj = roles.get_role_obj(role)
        statements += role_obj.get_all_statements(player_obj.player_index)
    return statements
