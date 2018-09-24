''' reg_wolf.py '''
import const
from ...village import Villager, Mason, Seer, Robber, Troublemaker, Drunk, Insomniac

# TODO: check better confining statements: if role in const.ROLE_SET and role not in stated_roles
def get_wolf_statements(player_index, wolf_indices, stated_roles, previous_statements):
    ''' Gets Regular Wolf statement. '''

    # role = self.center_role
    # if role != None and role != 'Wolf' and role != 'Mason':
    #     return self.get_center_wolf_statements(player_index, center_role, center_index, stated_roles)
    statements = []
    if 'Villager' in const.ROLE_SET:
        statements += Villager.get_villager_statements(player_index)
    if 'Insomniac' in const.ROLE_SET:
        statements += Insomniac.get_insomniac_statements(player_index, 'Insomniac')
    if 'Mason' in const.ROLE_SET:
        # Only say you are a Mason if you are the last player and there are no Masons.
        if player_index == const.NUM_PLAYERS - 1:
            mason_indices = [player_index]
            for i, stated_role in enumerate(stated_roles):
                if stated_role == 'Mason':
                    mason_indices.append(i)
            if len(mason_indices) == 1:
                statements += Mason.get_mason_statements(player_index, mason_indices)
    if 'Drunk' in const.ROLE_SET:
        for k in range(const.NUM_CENTER):
            statements += Drunk.get_drunk_statements(player_index, k + const.NUM_PLAYERS)
    if 'Troublemaker' in const.ROLE_SET:  # and 'Troublemaker' not in stated_roles:
        for i in range(len(stated_roles)):
            for j in range(i+1, len(stated_roles)):
                if j not in wolf_indices:
                    statements += Troublemaker.get_troublemaker_statements(player_index, i, j)
    if 'Robber' in const.ROLE_SET:
        for i, stated_role in enumerate(stated_roles):
            statements += Robber.get_robber_statements(player_index, i, stated_role)
    if 'Seer' in const.ROLE_SET:
        for i, stated_role in enumerate(stated_roles):
            if i not in wolf_indices and stated_role != 'Seer':      # 'Hey, I'm a Seer and I saw another Seer...'
                statements += Seer.get_seer_statements(player_index, i, stated_role)
    return statements
