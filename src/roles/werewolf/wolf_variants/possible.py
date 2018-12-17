''' possible.py '''
import const
from ...village import Villager, Mason, Seer, Robber, Troublemaker, Drunk, Insomniac

def get_expected_statements():
    '''
    Gets all possible statements that can be made by a village player from any index.
    Used to find the 'expect' part of the Expectimax algorithm.
    Returns set of statement objects.
    '''
    possible = {}
    for player_index in range(const.NUM_PLAYERS):
        possible[player_index] = []
        role_types = (Villager, Mason, Seer, Robber, Troublemaker, Drunk, Insomniac)
        for Role in role_types:
            if Role.__name__ in const.ROLE_SET:
                possible[player_index] += Role.get_all_statements(player_index)
    return possible
