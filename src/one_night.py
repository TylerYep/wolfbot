from roles import Wolf, Villager, Mason, Seer, Robber, Troublemaker, Drunk, Insomniac
from predictions import make_predictions, make_evil_prediction, print_guesses
from statistics import GameResult
from const import logger
from collections import defaultdict
from encoder import WolfBotEncoder
from util import find_all_player_indices, swap_characters, print_roles
import json
import const
import random

def play_one_night_werewolf(solver):
    ''' Plays one round of One Night Ultimate Werewolf. '''
    game_roles = list(const.ROLES)
    random.shuffle(game_roles)
    global ORIGINAL_ROLES
    ORIGINAL_ROLES = list(game_roles)
    wolf_inds = find_all_player_indices(game_roles, 'Wolf')

    player_objs = night_falls(game_roles)

    logger.info('\n -- GAME BEGINS -- \n')
    all_statements = get_statements(player_objs)
    print_roles(game_roles)

    save_game = [ORIGINAL_ROLES, game_roles, all_statements]
    with open('data/replay.json', 'w') as f: json.dump(save_game, f, cls=WolfBotEncoder)

    if const.USE_VOTING:
        all_role_guesses_arr = []
        for i in range(const.NUM_PLAYERS):
            # Good player vs Bad player guesses
            # TODO what happens when a wolf becomes good?
            if i in wolf_inds or player_objs[i].new_role == 'Wolf':
                all_solutions = solver(all_statements, i)
                prediction = make_evil_prediction(all_solutions)
            else:
                all_solutions = solver(all_statements, i)
                prediction = make_predictions(all_solutions)
            # print(prediction)
            all_role_guesses_arr.append(prediction)
        all_role_guesses, confidence = get_voting_result(all_role_guesses_arr)
        print_guesses(all_role_guesses)
        return GameResult(game_roles, all_role_guesses, all_statements, wolf_inds, confidence)
    else:
        all_solutions = solver(all_statements)
        # for solution in all_solutions:
        #     logger.debug('Solver interpretation: ' + str(solution.path))
        all_role_guesses = make_predictions(all_solutions)
        print_guesses(all_role_guesses)
        return GameResult(game_roles, all_role_guesses, all_statements, wolf_inds)

def get_voting_result(all_role_guesses_arr):
    ''' Take most common role guess as the final guess for that index. '''
    all_role_guesses, confidence = [], []
    for i in range(const.NUM_ROLES):
        role_dict = defaultdict(int)
        for prediction in all_role_guesses_arr:
            role_dict[prediction[i]] += 1
        role, count = max(role_dict.items(), key=lambda x: x[1])
        all_role_guesses.append(role)
        confidence.append(count / const.NUM_PLAYERS)
    return all_role_guesses, confidence

def get_statements(player_objs):
    ''' Returns array of each player's statements. '''
    stated_roles, given_statements = [], []
    for j in range(const.NUM_PLAYERS):
        statement = player_objs[j].get_statement(stated_roles, given_statements)
        stated_roles.append(statement.speaker)
        given_statements.append(statement)
        logger.info('Player ' + str(j) + ': ' + str(statement.sentence))
    return given_statements

def init_roles(game_roles, player_objs, Role):
    role_str = Role.__name__
    wake(role_str)
    for i in range(const.NUM_PLAYERS):
        if ORIGINAL_ROLES[i] == role_str:
            player_objs[i] = Role(i, game_roles, ORIGINAL_ROLES)
    sleep(role_str)

def night_falls(game_roles):
    ''' Initialize role object list and perform all switching and peeking actions to begin. '''
    logger.info('\n -- NIGHT FALLS -- \n')
    print_roles(game_roles)

    # Players perform actions on game_roles and add objects to list
    player_objs = list(game_roles)
    AWAKE_ORDER = (Wolf, Mason, Seer, Robber, Troublemaker, Drunk, Insomniac)
    for role in AWAKE_ORDER:
        init_roles(game_roles, player_objs, role)

    for i in range(const.NUM_PLAYERS):
        if ORIGINAL_ROLES[i] in ['Villager', 'Hunter']:
            player_objs[i] = Villager(i)

    return player_objs[:const.NUM_PLAYERS]

# TODO: convert to plurals
def wake(role_str):
    logger.info(role_str + ', wake up.')

def sleep(role_str):
    logger.info(role_str + ', go to sleep.\n')

def override_wolf_index(game_roles, wolf_inds):
    if const.FIXED_WOLF_INDEX != None:
        if len(wolf_inds) != 0:
            wolf_ind = random.choice(wolf_inds)
            swap_characters(game_roles, wolf_ind, const.FIXED_WOLF_INDEX)
