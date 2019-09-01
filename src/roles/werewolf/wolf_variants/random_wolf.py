''' random_wolf.py '''
from typing import List, Type

from src.statements import Statement
from src import const, roles

from ...village import Player

# Random Wolf Player
def get_wolf_statements_random(player_obj: Type[Player]) -> List[Statement]:
    ''' Gets Random Wolf statement '''
    statements = []
    for role in const.VILLAGE_ROLES:
        role_obj = roles.get_role_obj(role)
        statements += role_obj.get_all_statements(player_obj.player_index)
    return statements
