""" reg_wolf.py """
from typing import Any, Dict, Tuple

from src import const
from src.const import Role
from src.roles import (
    Drunk,
    Hunter,
    Insomniac,
    Mason,
    Robber,
    Seer,
    Troublemaker,
    Villager,
)
from src.statements import KnowledgeBase, Statement
from src.util import weighted_coin_flip


def should_include_role(counts_dict: Dict[Role, int], role: Role) -> bool:
    return counts_dict[role] > 0 or weighted_coin_flip(const.INCLUDE_STATEMENT_RATE)


def get_wolf_statements(
    player_obj: Any, knowledge_base: KnowledgeBase
) -> Tuple[Statement, ...]:
    """
    Gets Regular Wolf statement. Includes custom logic to maximize Wolf win rate.
    """
    statements: Tuple[Statement, ...] = ()
    stated_roles = knowledge_base.stated_roles
    player_index = player_obj.player_index
    counts_dict = dict(const.ROLE_COUNTS)
    for role in stated_roles:
        if role is not Role.NONE:
            counts_dict[role] -= 1

    if Role.VILLAGER in const.ROLE_SET and should_include_role(
        counts_dict, Role.VILLAGER
    ):
        statements += Villager.get_villager_statements(player_index)
    if Role.HUNTER in const.ROLE_SET and should_include_role(counts_dict, Role.HUNTER):
        statements += Hunter.get_hunter_statements(player_index)
    if Role.INSOMNIAC in const.ROLE_SET and should_include_role(
        counts_dict, Role.INSOMNIAC
    ):
        # TODO check for switches and prioritize those statements
        statements += Insomniac.get_insomniac_statements(player_index, Role.INSOMNIAC)
    if Role.MASON in const.ROLE_SET and should_include_role(counts_dict, Role.MASON):
        # Only say you are a Mason if you are the last player and there are no Masons.
        if player_index == const.NUM_PLAYERS - 1 and Role.MASON not in stated_roles:
            statements += Mason.get_mason_statements(player_index, (player_index,))
    if Role.DRUNK in const.ROLE_SET and should_include_role(counts_dict, Role.DRUNK):
        statements += Drunk.get_all_statements(player_index)
    if Role.TROUBLEMAKER in const.ROLE_SET and should_include_role(
        counts_dict, Role.TROUBLEMAKER
    ):
        num_stated = len(stated_roles)
        for i in range(num_stated):
            for j in range(i + 1, num_stated):
                # Do not reference a Wolf as the second index.
                if j not in player_obj.wolf_indices:
                    statements += Troublemaker.get_troublemaker_statements(
                        player_index, i, j
                    )
    if Role.ROBBER in const.ROLE_SET and should_include_role(counts_dict, Role.ROBBER):
        for i, stated_role in enumerate(stated_roles):
            if stated_role not in (Role.NONE, Role.ROBBER):
                # Only say you robbed a Seer if the real
                # Seer did not reference a Robber.
                if stated_role is Role.SEER:
                    use_index = True
                    for _, poss_set in knowledge_base.all_statements[i].knowledge:
                        if Role.ROBBER in poss_set:
                            use_index = False
                            break
                    if not use_index:
                        continue
                statements += Robber.get_robber_statements(player_index, i, stated_role)
    if Role.SEER in const.ROLE_SET and should_include_role(counts_dict, Role.SEER):
        for i, stated_role in enumerate(stated_roles):
            # 'Hey, I'm a Seer and I saw another Seer...'
            if (
                stated_role not in (Role.NONE, Role.SEER)
                and i not in player_obj.wolf_indices
            ):
                statements += Seer.get_seer_statements(player_index, (i, stated_role))
    return statements
