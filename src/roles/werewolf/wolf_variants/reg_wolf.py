""" reg_wolf.py """
from typing import Any, Tuple

from src import const
from src.roles.village import Drunk, Hunter, Insomniac, Mason, Robber, Seer, Troublemaker, Villager
from src.statements import KnowledgeBase, Statement


def get_wolf_statements(player_obj: Any, knowledge_base: KnowledgeBase) -> Tuple[Statement, ...]:
    """ Gets Regular Wolf statement. Includes custom logic to maximize Wolf win rate. """
    statements: Tuple[Statement, ...] = ()
    stated_roles = knowledge_base.stated_roles
    previous_statements = knowledge_base.all_statements
    player_index = player_obj.player_index
    wolf_indices = player_obj.wolf_indices
    if "Villager" in const.ROLE_SET:
        statements += Villager.get_villager_statements(player_index)
    if "Hunter" in const.ROLE_SET:
        statements += Hunter.get_hunter_statements(player_index)
    if "Insomniac" in const.ROLE_SET:
        # TODO check for switches and prioritize those statements
        statements += Insomniac.get_insomniac_statements(player_index, "Insomniac")
    if "Mason" in const.ROLE_SET:
        # Only say you are a Mason if you are the last player and there are no Masons.
        if player_index == const.NUM_PLAYERS - 1 and "Mason" not in stated_roles:
            statements += Mason.get_mason_statements(player_index, (player_index,))
    if "Drunk" in const.ROLE_SET:
        for k in range(const.NUM_CENTER):
            statements += Drunk.get_drunk_statements(player_index, k + const.NUM_PLAYERS)
    if "Troublemaker" in const.ROLE_SET:
        num_stated = len(stated_roles)
        for i in range(num_stated):
            for j in range(i + 1, num_stated):
                # Do not reference a Wolf as the second index.
                if j not in wolf_indices:
                    statements += Troublemaker.get_troublemaker_statements(player_index, i, j)
    if "Robber" in const.ROLE_SET:
        for i, stated_role in enumerate(stated_roles):
            if stated_role and stated_role != "Robber":
                # Only say you robbed a Seer if the real Seer did not reference a Robber.
                if stated_role == "Seer":
                    use_index = True
                    for _, poss_set in previous_statements[i].knowledge:
                        if "Robber" in poss_set:
                            use_index = False
                    if not use_index:
                        continue
                statements += Robber.get_robber_statements(player_index, i, stated_role)
    if "Seer" in const.ROLE_SET:
        for i, stated_role in enumerate(stated_roles):
            # 'Hey, I'm a Seer and I saw another Seer...'
            if stated_role and i not in wolf_indices and stated_role != "Seer":
                statements += Seer.get_seer_statements(player_index, (i, stated_role))
    return statements
