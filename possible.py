from roles import *
import const

def get_possible_statements(role_set=const.ROLE_SET):
    possible = {}
    for player_index in range(const.NUM_PLAYERS):
        possible[player_index] = Villager.get_villager_statements(player_index)
        
        if 'Drunk' in role_set:
            for k in range(const.NUM_CENTER):
                possible[player_index] += Drunk.get_drunk_statements(player_index, k + const.NUM_PLAYERS)

        for i in range(const.NUM_PLAYERS):
            if 'Mason' in role_set:
                if player_index != i:
                    mason_indices = [player_index, i]
                    possible[player_index]+= Mason.get_mason_statements(player_index, mason_indices)
            if 'Troublemaker' in role_set:
                for j in range(const.NUM_PLAYERS): # Troublemaker should not refer to other wolves or themselves
                    if i != j != player_index and i != player_index: #and i not in wolf_indices and j not in wolf_indices:
                        possible[player_index] += Troublemaker.get_troublemaker_statements(player_index, i, j)

            # Wolf-seer more likely to declare they saw a villager
            for role in const.ROLES:
                if role != 'Seer': # "Hey, I'm a Seer and I saw another Seer..."
                    if i != player_index:
                        possible[player_index]+= Seer.get_seer_statements(player_index, i, role)
                if 'Robber' in role_set:
                    if role != 'Wolf':      # "I robbed a Wolf and now I'm a Wolf..."
                        possible[player_index]+= Robber.get_robber_statements(player_index, i, role)
    return possible
