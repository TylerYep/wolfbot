''' util.py '''
import random
from src import const
from src.const import logger

def swap_characters(game_roles, i, j):
    ''' Util function to swap two characters, updating game_roles. '''
    temp = game_roles[i]
    game_roles[i] = game_roles[j]
    game_roles[j] = temp


def find_all_player_indices(game_roles, role):
    ''' Util function to find all indices of a given role. '''
    return [i for i in range(const.NUM_PLAYERS) if game_roles[i] == role]


def get_player(self_obj, vals_to_exclude=()):
    ''' Gets a random player index (not in the center). '''
    return input_player(vals_to_exclude) if self_obj.is_user else get_random_player(vals_to_exclude)


def get_center(self_obj, vals_to_exclude=()):
    ''' Gets a random index of a center card. '''
    return input_center(vals_to_exclude) if self_obj.is_user else get_random_center(vals_to_exclude)


def get_random_player(vals_to_exclude=()):
    ''' Gets a random player index (not in the center). '''
    choice_ind = -1
    while choice_ind == -1 or choice_ind in vals_to_exclude:
        choice_ind = random.randint(0, const.NUM_PLAYERS - 1)
    return choice_ind


def get_random_center(vals_to_exclude=()):
    ''' Gets a random index of a center card. '''
    choice_ind = -1
    while choice_ind == -1 or choice_ind in vals_to_exclude:
        choice_ind = const.NUM_PLAYERS + random.randint(0, const.NUM_CENTER - 1)
    return choice_ind


def input_player(vals_to_exclude=()):
    ''' Prompts the user for a player index (not in the center). '''
    choice_ind = -1
    while choice_ind < 0 or choice_ind >= const.NUM_PLAYERS:
        user_input = ''
        while not user_input.isdigit():
            user_input = input(f'Which player index (0-{const.NUM_PLAYERS - 1})? ')
        choice_ind = int(user_input)

        if choice_ind in vals_to_exclude:
            logger.info('You cannot choose yourself or any index twice.')
            choice_ind = -1
    return choice_ind


def input_center(vals_to_exclude=()):
    ''' Prompts the user for a center card index. '''
    choice_ind = -1
    while choice_ind < 0 or choice_ind >= const.NUM_CENTER:
        user_input = ''
        while not user_input.isdigit():
            user_input = input(f'Which center card (0-{const.NUM_CENTER - 1})? ')
        choice_ind = int(user_input)

        if choice_ind + const.NUM_PLAYERS in vals_to_exclude:
            logger.info('You cannot choose any index twice.')
            choice_ind = -1
    return choice_ind + const.NUM_PLAYERS


def get_numeric_input(size):
    ''' Prompts the user for an index between 0 and size. '''
    choice_ind = -1
    while choice_ind < 0 or choice_ind >= size:
        user_input = ''
        while not user_input.isdigit():
            user_input = input(f'Enter a number from 0-{size - 1}: ')
        choice_ind = int(user_input)
    return choice_ind


def print_roles(game_roles):
    ''' Formats hidden roles to console. '''
    logger.debug(f'[Hidden] Current roles: {game_roles[:const.NUM_PLAYERS]} \
                \n\t  Center cards: {game_roles[const.NUM_PLAYERS:]}\n'.replace('\'', ''))
