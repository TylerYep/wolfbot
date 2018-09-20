from roles import Villager, Mason, Seer, Robber, Troublemaker, Drunk, Insomniac
from wolf import Wolf
from predictions import make_predictions, make_evil_prediction, print_guesses
from statistics import GameResult
from const import logger
from collections import defaultdict
from encoder import WolfBotEncoder
import json
import const
import random

def override_wolf_index(game_roles, wolf_inds):
    if const.FIXED_WOLF_INDEX != None:
        if len(wolf_inds) != 0:
            wolf_ind = random.choice(wolf_inds)
            swap_characters(game_roles, wolf_ind, const.FIXED_WOLF_INDEX)

def play_one_night_werewolf(solver):
    ''' Plays one round of One Night Ultimate Werewolf. '''
    game_roles = list(const.ROLES)
    random.shuffle(game_roles)
    global ORIGINAL_ROLES
    ORIGINAL_ROLES = list(game_roles)

    wolf_inds = find_all_player_indices(game_roles, 'Wolf')
    # override_wolf_index(game_roles, wolf_inds)

    player_objs = night_falls(game_roles)

    logger.info('\n -- GAME BEGINS -- \n')
    all_statements = get_statements(player_objs, wolf_inds)
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

def get_statements(player_objs, wolf_inds):
    ''' Returns array of each player's statements. '''
    stated_roles, given_statements = [], []
    for j in range(const.NUM_PLAYERS):
        statement = player_objs[j].get_statement(stated_roles, given_statements)
        # TODO: bug with RL wolf without a speaker field
        stated_roles.append(statement.speaker)
        given_statements.append(statement)
        logger.info('Player ' + str(j) + ': ' + str(statement.sentence))
    return given_statements

# Print out progress messages and initialize needed variables
def night_falls(game_roles):
    ''' Initialize role object list and perform all switching and peeking actions to begin. '''
    logger.info('\n -- NIGHT FALLS -- \n')
    print_roles(game_roles)

    # Players perform actions on game_roles and add objects to list
    player_objs = list(game_roles)
    wake('Wolves')
    for i in range(const.NUM_PLAYERS):
        if ORIGINAL_ROLES[i] == 'Wolf':
            player_objs[i] = Wolf(*wolf_init(i, game_roles))
    sleep('Wolves')
    wake('Masons')
    for i in range(const.NUM_PLAYERS):
        if ORIGINAL_ROLES[i] == 'Mason':
            player_objs[i] = Mason(*mason_init(i, game_roles))
    sleep('Masons')
    wake('Seer')
    for i in range(const.NUM_PLAYERS):
        if ORIGINAL_ROLES[i] == 'Seer':
            player_objs[i] = Seer(*seer_init(i, game_roles))
    sleep('Seer')
    wake('Robber')
    for i in range(const.NUM_PLAYERS):
        if ORIGINAL_ROLES[i] == 'Robber':
            player_objs[i] = Robber(*robber_init(i, game_roles))
    sleep('Robber')
    wake('Troublemaker')
    for i in range(const.NUM_PLAYERS):
        if ORIGINAL_ROLES[i] == 'Troublemaker':
            player_objs[i] = Troublemaker(*troublemaker_init(i, game_roles))
    sleep('Troublemaker')
    wake('Drunk')
    for i in range(const.NUM_PLAYERS):
        if ORIGINAL_ROLES[i] == 'Drunk':
            player_objs[i] = Drunk(*drunk_init(i, game_roles))
    sleep('Drunk')
    wake('Insomniac')
    for i in range(const.NUM_PLAYERS):
        if ORIGINAL_ROLES[i] == 'Insomniac':
            player_objs[i] = Insomniac(*insomniac_init(i, game_roles))
    sleep('Insomniac')

    # Initialize remaining characters TODO use function map? for Hunter too...
    for i in range(const.NUM_PLAYERS):
        if ORIGINAL_ROLES[i] == 'Villager':
            player_objs[i] = Villager(i)
    return player_objs[:const.NUM_PLAYERS]


def wolf_init(index, game_roles):
    ''' Initializes Wolf - gets Wolf indices and a random center card, if applicable. '''
    wolf_indices = set(find_all_player_indices(ORIGINAL_ROLES, 'Wolf'))
    wolf_center_index, wolf_center_role = None, None
    if len(wolf_indices) == 1 and const.NUM_CENTER > 0:
        wolf_center_index = get_random_center()
        wolf_center_role = game_roles[wolf_center_index]
    logger.debug('[Hidden] Wolves are at indices: ' + str(wolf_indices))
    return index, wolf_indices, wolf_center_index, wolf_center_role


def seer_init(index, game_roles):
    ''' Initializes Seer - either sees 2 center cards or 1 player card. '''
    # Picks two center cards more often, because that generally yields higher win rates.
    choose_center = random.choices([True, False], [0.9, 0.1])
    if choose_center and const.NUM_CENTER > 1:
        seer_peek_index = get_random_center()
        seer_peek_character = game_roles[seer_peek_index]
        seer_peek_index2 = get_random_center()
        while seer_peek_index2 == seer_peek_index:
            seer_peek_index2 = get_random_center()
        seer_peek_character2 = game_roles[seer_peek_index2]
        logger.debug('[Hidden] Seer sees that Center ' + str(seer_peek_index - const.NUM_PLAYERS) +
                ' is a ' + str(seer_peek_character) + ' and Center ' + str(seer_peek_index2 - const.NUM_PLAYERS) +
                ' is a ' + str(seer_peek_character2))
        return index, seer_peek_index, seer_peek_character, seer_peek_index2, seer_peek_character2
    else:
        seer_peek_index = get_random_player()
        while seer_peek_index == index:
            seer_peek_index = get_random_player()
        seer_peek_character = game_roles[seer_peek_index]
        logger.debug('[Hidden] Seer sees that Player ' + str(seer_peek_index) +
                ' is a ' + str(seer_peek_character))
        return index, seer_peek_index, seer_peek_character, None, None


def mason_init(index, game_roles):
    ''' Initializes Mason - sees all other Masons. '''
    mason_indices = find_all_player_indices(ORIGINAL_ROLES, 'Mason')
    logger.debug('[Hidden] Masons are at indices: ' + str(mason_indices))
    return index, mason_indices


def robber_init(index, game_roles):
    ''' Initializes Robber - switches roles with another player. '''
    robber_choice_index = get_random_player()
    while robber_choice_index == index:
        robber_choice_index = get_random_player()
    robber_choice_character = game_roles[robber_choice_index]
    logger.debug('[Hidden] Robber switches with Player ' + str(robber_choice_index) +
                ' and becomes a ' + str(robber_choice_character))
    swap_characters(game_roles, index, robber_choice_index)
    return index, robber_choice_index, robber_choice_character


def drunk_init(index, game_roles):
    ''' Initializes Drunk - switches with a card in the center. '''
    assert(const.NUM_CENTER != 0)
    drunk_choice_index = get_random_center()
    logger.debug('[Hidden] Drunk switches with Center Card ' + str(drunk_choice_index - const.NUM_PLAYERS) +
                ' and unknowingly becomes a ' + str(game_roles[drunk_choice_index]))
    swap_characters(game_roles, index, drunk_choice_index)
    return index, drunk_choice_index


def troublemaker_init(index, game_roles):
    ''' Initializes Troublemaker - switches one player with another player. '''
    troublemaker_choice_index1 = get_random_player()
    troublemaker_choice_index2 = get_random_player()
    while troublemaker_choice_index1 == index:
        troublemaker_choice_index1 = get_random_player()
    while troublemaker_choice_index2 == index or troublemaker_choice_index2 == troublemaker_choice_index1:
        troublemaker_choice_index2 = get_random_player()
    swap_characters(game_roles, troublemaker_choice_index1, troublemaker_choice_index2)
    logger.debug('[Hidden] Troublemaker switches Player ' + str(troublemaker_choice_index1)
        + ' with Player ' + str(troublemaker_choice_index2))
    return index, troublemaker_choice_index1, troublemaker_choice_index2


def insomniac_init(index, game_roles):
    ''' Initializes Insomniac - learns new role. '''
    insomniac_new_role = game_roles[index]
    logger.debug('[Hidden] Insomniac wakes up as a ' + insomniac_new_role)
    return index, insomniac_new_role


### Util functions ###

def swap_characters(game_roles, i, j):
    ''' Util function to swap two characters, updating game_roles and the player_set. '''
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

def wake(role):
    logger.info(role + ', wake up.')

def sleep(role):
    logger.info(role + ', go to sleep.\n')
