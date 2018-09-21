import const
import random
from const import logger

def swap_characters(game_roles, i, j):
    ''' Util function to swap two characters, updating game_roles. '''
    temp = game_roles[i]
    game_roles[i] = game_roles[j]
    game_roles[j] = temp


def find_all_player_indices(game_roles, role):
    ''' Util function to find all indices of a given role. '''
    return [i for i in range(const.NUM_PLAYERS) if game_roles[i] == role]


def get_random_player():
    ''' Gets a random player index (not in the center). '''
    return random.randint(0, const.NUM_PLAYERS - 1)


def get_random_center():
    ''' Gets a random index of a center card. '''
    return const.NUM_PLAYERS + random.randint(0, const.NUM_CENTER - 1)


def print_roles(game_roles):
    logger.debug('[Hidden] Current roles: ' + str(game_roles[:const.NUM_PLAYERS]) +
                '\n\t Center cards:  ' + str(game_roles[const.NUM_PLAYERS:]) + '\n')
