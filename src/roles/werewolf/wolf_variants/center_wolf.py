''' center_wolf.py '''
import const
from ...village import Villager, Seer, Robber, Troublemaker, Drunk, Insomniac

# Currently unused. This info is hard to use
def get_center_wolf_statements(player_index, center_role, center_index, wolf_indices, stated_roles):
    ''' Center Wolf Player logic. '''
    statements = []
    role = center_role
    if role == 'Villager':
        statements += Villager.get_villager_statements(player_index)
    elif role == 'Robber':
        for i, stated_role in enumerate(stated_roles):
            statements += Robber.get_robber_statements(player_index, i, stated_role)
    elif role == 'Troublemaker':
        for i in range(len(stated_roles)):
            for j in range(i+1, len(stated_roles)):
                if j not in wolf_indices:
                    statements += Troublemaker.get_troublemaker_statements(player_index, i, j)
    elif role == 'Drunk':
        statements += Drunk.get_drunk_statements(player_index, center_index)
    elif role == 'Insomniac':
        statements += Insomniac.get_insomniac_statements(player_index, 'Insomniac')
    elif role == 'Seer':
        for i, stated_role in enumerate(stated_roles):
            # 'Hey, I'm a Seer and I saw another Seer...'
            if i not in wolf_indices and stated_role != 'Seer':
                statements += Seer.get_seer_statements(player_index, i, stated_role)
        for c1 in range(const.NUM_CENTER):
            for c2 in range(c1 + 1, const.NUM_CENTER):
                for role1 in const.ROLES:
                    for role2 in const.ROLES:
                        if role1 != 'Seer' and role2 != 'Seer':
                            if role1 != role2 or const.ROLE_COUNTS[role1] >= 2:
                                statements += Seer.get_seer_statements(player_index, c1  + const.NUM_PLAYERS,
                                                                       role1, c2 + const.NUM_PLAYERS, role2)
    return statements
