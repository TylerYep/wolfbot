''' reg_wolf.py '''
import const
from ...village import Villager, Mason, Seer, Robber, Troublemaker, Drunk, Insomniac, Hunter

def get_wolf_statements(player_obj, stated_roles, previous_statements):
    ''' Gets Regular Wolf statement. '''
    statements = []
    player_index = player_obj.player_index
    wolf_indices = player_obj.wolf_indices
    if 'Villager' in const.ROLE_SET:
        statements += Villager.get_villager_statements(player_index)
    if 'Hunter' in const.ROLE_SET:
        statements += Hunter.get_hunter_statements(player_index)
    if 'Insomniac' in const.ROLE_SET:
        # TODO check for switches and prioritize those statements
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
    if 'Troublemaker' in const.ROLE_SET:
        for i in range(len(stated_roles)):
            for j in range(i+1, len(stated_roles)):
                if j not in wolf_indices:
                    statements += Troublemaker.get_troublemaker_statements(player_index, i, j)
    if 'Robber' in const.ROLE_SET:
        for i, stated_role in enumerate(stated_roles):
            if stated_role != 'Robber':
                if stated_role == 'Seer':
                    use_index = True
                    for _, poss_set in previous_statements[i].knowledge:
                        if 'Robber' in poss_set:
                            use_index = False
                    if not use_index:
                        continue
                statements += Robber.get_robber_statements(player_index, i, stated_role)
    if 'Seer' in const.ROLE_SET:
        for i, stated_role in enumerate(stated_roles):
            # 'Hey, I'm a Seer and I saw another Seer...'
            if i not in wolf_indices and stated_role != 'Seer':
                statements += Seer.get_seer_statements(player_index, i, stated_role)
    return statements
