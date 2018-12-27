''' random_wolf.py '''
import const
from ...village import Villager, Mason, Seer, Robber, Troublemaker, Drunk, Insomniac, Hunter

# Random Wolf Player
def get_wolf_statements_random(player_obj):
    ''' Gets Random Wolf statement '''
    statements = []
    player_index = player_obj.player_index

    role_types = (Villager, Mason, Seer, Robber, Troublemaker, Drunk, Insomniac, Hunter)
    for Role in role_types:
        if Role.__name__ in const.ROLE_SET:
            statements += Role.get_all_statements(player_index)
    return statements
