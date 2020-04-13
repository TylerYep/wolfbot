''' center_wolf.py '''
from typing import Any, List

from src import const
from src.statements import Statement

from ...village import Drunk, Hunter, Insomniac, Robber, Seer, Troublemaker, Villager


def get_center_wolf_statements(player_obj: Any,
                               stated_roles: List[str]) -> List[Statement]:
    ''' Center Wolf Player logic. '''
    statements: List[Statement] = []
    player_index = player_obj.player_index
    wolf_indices = player_obj.wolf_indices
    center_role = player_obj.center_role
    center_index = player_obj.center_index

    if center_role == 'Villager':
        statements += Villager.get_villager_statements(player_index)
    elif center_role == 'Hunter':
        statements += Hunter.get_hunter_statements(player_index)
    elif center_role == 'Insomniac':
        # TODO check for switches and prioritize those statements
        statements += Insomniac.get_insomniac_statements(player_index, 'Insomniac')
    elif center_role == 'Robber':
        for i, stated_role in enumerate(stated_roles):
            if stated_role != 'Robber':
                statements += Robber.get_robber_statements(player_index, i, stated_role)
    elif center_role == 'Troublemaker':
        for i in range(len(stated_roles)):
            for j in range(i + 1, len(stated_roles)):
                if j not in wolf_indices:
                    statements += Troublemaker.get_troublemaker_statements(player_index, i, j)
    elif center_role == 'Drunk':
        statements += Drunk.get_drunk_statements(player_index, center_index)
    elif center_role == 'Seer':
        for i, stated_role in enumerate(stated_roles):
            # 'Hey, I'm a Seer and I saw another Seer...'
            if i not in wolf_indices and stated_role != 'Seer':
                statements += Seer.get_seer_statements(player_index, (i, stated_role))
        for role2 in const.ROLES:
            for cent1 in range(const.NUM_CENTER):
                if cent1 != center_index:
                    for role1 in const.ROLES:
                        if role1 != 'Seer' and role2 != 'Seer':
                            if role1 != role2 or const.ROLE_COUNTS[role1] >= 2:
                                choice_1 = (cent1 + const.NUM_PLAYERS, role1)
                                choice_2 = (center_index, role2)
                                statements += Seer.get_seer_statements(player_index,
                                                                       choice_1,
                                                                       choice_2)
    return statements
