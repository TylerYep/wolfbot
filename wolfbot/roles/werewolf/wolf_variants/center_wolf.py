""" center_wolf.py """
from typing import Any

from wolfbot import const
from wolfbot.enums import Role
from wolfbot.roles import Drunk, Hunter, Insomniac, Robber, Seer, Troublemaker, Villager
from wolfbot.statements import KnowledgeBase, Statement


def get_center_wolf_statements(
    player_obj: Any, knowledge_base: KnowledgeBase
) -> tuple[Statement, ...]:
    """Center Wolf Player logic."""
    statements: tuple[Statement, ...] = ()
    player_index = player_obj.player_index
    wolf_indices = player_obj.wolf_indices
    center_role = player_obj.center_role
    center_index = player_obj.center_index

    if center_role is Role.VILLAGER:
        statements += Villager.get_villager_statements(player_index)
    elif center_role is Role.HUNTER:
        statements += Hunter.get_hunter_statements(player_index)
    elif center_role is Role.INSOMNIAC:
        # TODO check for switches and prioritize those statements
        statements += Insomniac.get_insomniac_statements(player_index, Role.INSOMNIAC)
    elif center_role is Role.ROBBER:
        for i, stated_role in enumerate(knowledge_base.stated_roles):
            if stated_role not in (Role.NONE, Role.ROBBER):
                statements += Robber.get_robber_statements(player_index, i, stated_role)
    elif center_role is Role.TROUBLEMAKER:
        num_stated = len(knowledge_base.stated_roles)
        for i in range(num_stated):
            for j in range(i + 1, num_stated):
                if j not in wolf_indices:
                    statements += Troublemaker.get_troublemaker_statements(
                        player_index, i, j
                    )
    elif center_role is Role.DRUNK:
        statements += Drunk.get_drunk_statements(player_index, center_index)
    elif center_role is Role.SEER:
        for i, stated_role in enumerate(knowledge_base.stated_roles):
            # 'Hey, I'm a Seer and I saw another Seer...'
            if i not in wolf_indices and stated_role not in (Role.NONE, Role.SEER):
                statements += Seer.get_seer_statements(player_index, (i, stated_role))
        for role2 in const.SORTED_ROLE_SET:
            for cent1 in range(const.NUM_CENTER):
                if cent1 != center_index:
                    for role1 in const.SORTED_ROLE_SET:
                        if role1 is not Role.SEER and role2 is not Role.SEER:
                            if role1 != role2 or const.ROLE_COUNTS[role1] >= 2:
                                statements += Seer.get_seer_statements(
                                    player_index,
                                    (cent1 + const.NUM_PLAYERS, role1),
                                    (center_index, role2),
                                )
    return statements
