''' one_night.py '''
import random
import json

from roles import Wolf, Minion, Villager, Mason, Seer, Robber, Troublemaker, Drunk, \
                    Insomniac, Tanner, Hunter
from encoder import WolfBotEncoder
from util import find_all_player_indices, swap_characters, print_roles
from voting import consolidate_results
from const import logger
import const

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
    print_roles(game_roles)

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


def init_roles(game_roles, player_objs, Role):
    ''' Interates through each player in player_objs and initializes the Player object. '''
    role_str = Role.__name__
    logger.info('%s, wake up.', role_str)
    for i in range(const.NUM_PLAYERS):
        if ORIGINAL_ROLES[i] == role_str:
            player_objs[i] = Role(i, game_roles, ORIGINAL_ROLES)
    logger.info('%s, go to sleep.\n', role_str)


def night_falls(game_roles):
    ''' Initialize role object list and perform all switching and peeking actions to begin. '''
    logger.info('\n -- NIGHT FALLS -- \n')
    print_roles(game_roles)

    # Awaken each player in order (print command)
    player_objs = list(game_roles)
    awake_order = (Wolf, Minion, Mason, Seer, Robber, Troublemaker, Drunk, Insomniac)
    for role in awake_order:
        # role =
        init_roles(game_roles, player_objs, role)

    # All other players wake up at the same time
    for i in range(const.NUM_PLAYERS):
        if ORIGINAL_ROLES[i] == 'Tanner':
            player_objs[i] = Tanner(i, game_roles, ORIGINAL_ROLES)
        elif ORIGINAL_ROLES[i] == 'Villager':
            player_objs[i] = Villager(i, game_roles, ORIGINAL_ROLES)
        elif ORIGINAL_ROLES[i] == 'Hunter':
            player_objs[i] = Hunter(i, game_roles, ORIGINAL_ROLES)

    return player_objs[:const.NUM_PLAYERS]


def override_wolf_index(game_roles):
    ''' Swap a Wolf to the const.FIXED_WOLF_INDEX. '''
    wolf_inds = find_all_player_indices(game_roles, 'Wolf')
    if wolf_inds:
        wolf_ind = random.choice(wolf_inds)
        swap_characters(game_roles, wolf_ind, const.FIXED_WOLF_INDEX)
