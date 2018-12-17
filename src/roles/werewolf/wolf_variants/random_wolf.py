''' random_wolf.py '''
import const
from ...village import Villager, Mason, Seer, Robber, Troublemaker, Drunk, Insomniac

# Random Wolf Player
def get_wolf_statements_random(player_obj):
    ''' Gets Random Wolf statement (all completely stupid statements are removed) '''
    statements = []
    player_index = player_obj.player_index
    wolf_indices = player_obj.wolf_indices
    if 'Villager' in const.ROLE_SET:
        statements += Villager.get_villager_statements(player_index)
    if 'Insomniac' in const.ROLE_SET:
        for role in const.ROLES:
            if role != 'Wolf':
                statements += Insomniac.get_insomniac_statements(player_index, role)
    if 'Mason' in const.ROLE_SET:
        statements += Mason.get_mason_statements(player_index, [player_index])
        for i in range(const.NUM_PLAYERS):
            if player_index != i:
                mason_indices = [player_index, i]
                statements += Mason.get_mason_statements(player_index, mason_indices)
    if 'Drunk' in const.ROLE_SET:
        for k in range(const.NUM_CENTER):
            statements += Drunk.get_drunk_statements(player_index, k + const.NUM_PLAYERS)
    if 'Troublemaker' in const.ROLE_SET:
        for i in range(const.NUM_PLAYERS):
            for j in range(i+1, const.NUM_PLAYERS):
                # Troublemaker should not refer to other wolves or themselves
                if i != j != player_index and i != player_index and i not in wolf_indices and j not in wolf_indices:
                    statements += Troublemaker.get_troublemaker_statements(player_index, i, j)
    if 'Robber' in const.ROLE_SET:
        for i in range(const.NUM_PLAYERS):
            for role in const.ROLES:
                if role not in ('Wolf', 'Robber') and player_index != i:      # 'I robbed Player 0 and now I'm a Wolf...'
                    statements += Robber.get_robber_statements(player_index, i, role)
    if 'Seer' in const.ROLE_SET:
        for role in const.ROLES:
            for i in range(const.NUM_PLAYERS):
                if i not in wolf_indices and role != 'Seer':      # 'Hey, I'm a Seer and I saw another Seer...'
                    statements += Seer.get_seer_statements(player_index, i, role)
        # Wolf using these usually gives himself away
        for c1 in range(const.NUM_CENTER):
            for c2 in range(c1 + 1, const.NUM_CENTER):
                for role1 in const.ROLES:
                    for role2 in const.ROLES:
                        if role1 != 'Seer' and role2 != 'Seer':
                            if role1 != role2 or const.ROLE_COUNTS[role1] >= 2:
                                statements += Seer.get_seer_statements(player_index, c1  + const.NUM_PLAYERS,
                                                                       role1, c2 + const.NUM_PLAYERS, role2)
    return statements
