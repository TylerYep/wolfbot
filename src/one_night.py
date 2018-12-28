''' one_night.py '''
import random
import json

from encoder import WolfBotEncoder
from roles import get_role_obj
from voting import consolidate_results
from const import logger
import const
import util

def play_one_night_werewolf(save_replay=True):
    ''' Plays one round of One Night Ultimate Werewolf. '''
    global ORIGINAL_ROLES
    game_roles = list(const.ROLES)
    if const.RANDOMIZE_ROLES:
        random.shuffle(game_roles)
    ORIGINAL_ROLES = list(game_roles)
    if const.FIXED_WOLF_INDEX is not None:
        override_wolf_index(game_roles)

    player_objs = night_falls(game_roles)
    logger.info('\n -- GAME BEGINS -- \n')
    all_statements = get_player_statements(player_objs)
    util.print_roles(game_roles)

    save_game = (ORIGINAL_ROLES, game_roles, all_statements, player_objs)
    if save_replay:
        with open('data/replay.json', 'w') as f_replay:
            json.dump(save_game, f_replay, cls=WolfBotEncoder)

    return consolidate_results(save_game)


def get_player_statements(player_objs):
    ''' Returns array of each player's statements. '''
    stated_roles, given_statements = [], []
    for j in range(const.NUM_PLAYERS):
        statement = player_objs[j].get_statement(stated_roles, given_statements)
        stated_roles.append(statement.speaker)
        given_statements.append(statement)
        logger.info('Player %d: %s', j, statement.sentence)
    return given_statements


def awaken_role(game_roles, player_objs, role_str):
    ''' Interates through each player in player_objs and initializes the Player object. '''
    logger.info('%s, wake up.', role_str)
    role_obj = get_role_obj(role_str)
    for i in range(const.NUM_PLAYERS):
        if ORIGINAL_ROLES[i] == role_str:
            player_objs[i] = role_obj(i, game_roles, ORIGINAL_ROLES)
    logger.info('%s, go to sleep.\n', role_str)


def night_falls(game_roles):
    ''' Initialize role object list and perform all switching and peeking actions to begin. '''
    logger.info('\n -- NIGHT FALLS -- \n')
    util.print_roles(game_roles)

    # Awaken each player in order (print command)
    player_objs = list(game_roles)
    for role in const.AWAKE_ORDER:
        awaken_role(game_roles, player_objs, role)

    # All other players wake up at the same time
    for i, role in enumerate(ORIGINAL_ROLES):
        if role in const.ROLE_SET - set(const.AWAKE_ORDER):
            role_obj = get_role_obj(role)
            player_objs[i] = role_obj(i, game_roles, ORIGINAL_ROLES)

    return player_objs[:const.NUM_PLAYERS]


def override_wolf_index(game_roles):
    ''' Swap a Wolf to the const.FIXED_WOLF_INDEX. '''
    wolf_inds = util.find_all_player_indices(game_roles, 'Wolf')
    if wolf_inds:
        wolf_ind = random.choice(wolf_inds)
        util.swap_characters(game_roles, wolf_ind, const.FIXED_WOLF_INDEX)
