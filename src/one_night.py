from roles import Villager, Mason, Seer, Robber, Troublemaker, Drunk, Insomniac
from wolf import Wolf
from predictions import make_predictions, make_evil_prediction, print_guesses
from statistics import GameResult
from const import logger
from collections import defaultdict
import const
import pickle
import random

def play_one_night_werewolf(solver):
    ''' Plays one round of One Night Ultimate Werewolf. '''
    global game_roles, original_roles, player_set
    game_roles = list(const.ROLES)
    random.shuffle(game_roles)

    wolf_inds = find_all_player_indices('Wolf')
    if const.FIXED_WOLF_INDEX != None:
        if len(wolf_inds) != 0:
            wolf_ind = random.choice(wolf_inds)
            swap_characters(wolf_ind, const.FIXED_WOLF_INDEX)

    player_set = set(game_roles[:const.NUM_PLAYERS])
    original_roles = list(game_roles)

    player_objs = night_falls()
    logger.info("\n -- GAME BEGINS -- \n")
    all_statements = get_statements(player_objs, wolf_inds)
    print_roles()

    save_game = [original_roles, game_roles, all_statements]
    with open('data/replay.pkl', 'wb') as f: pickle.dump(save_game, f)

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
        #     logger.debug("Solver interpretation: " + str(solution.path))
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
        logger.info("Player " + str(j) + ": " + str(statement.sentence))
    return given_statements

# Print out progress messages and initialize needed variables
def night_falls():
    ''' Initialize role object array and perform all switching and peeking actions to begin. '''
    logger.info("\n -- NIGHT FALLS -- \n")
    print_roles()
    if 'Insomniac' in player_set:
        insomniac_ind = original_roles.index('Insomniac')
    wake('Wolves')
    if 'Wolf' in player_set:
        wolf_indices, wolf_center_index, wolf_center_role = wolf_init()
    sleep('Wolves')
    wake('Masons')
    if 'Mason' in player_set:
        mason_indices = mason_init()
    sleep('Masons')
    wake('Seer')
    if 'Seer' in player_set:
        seer_peek_index, seer_peek_character, seer_peek_index2, seer_peek_character2 = seer_init()
    sleep('Seer')
    wake('Robber')
    if 'Robber' in player_set:
        robber_choice_index, robber_choice_character = robber_init()
    sleep('Robber')
    wake('Troublemaker')
    if 'Troublemaker' in player_set:
        trblmkr_index1, trblmkr_index2 = troublemaker_init()
    sleep('Troublemaker')
    wake('Drunk')
    if 'Drunk' in player_set:
        drunk_choice_index = drunk_init()
    sleep('Drunk')
    wake('Insomniac')
    if 'Insomniac' in player_set:
        insomniac_new_role = insomniac_init(insomniac_ind)
    sleep('Insomniac')

    # Initialize players
    players = []
    for i in range(const.NUM_ROLES):
        role = original_roles[i]
        if i >= const.NUM_PLAYERS: players.append(role)      # Center cards
        elif role == 'Wolf': players.append(Wolf(i, wolf_indices, wolf_center_index, wolf_center_role))
        elif role == 'Villager': players.append(Villager(i))
        elif role == 'Robber': players.append(Robber(i, robber_choice_index, robber_choice_character))
        elif role == 'Mason': players.append(Mason(i, mason_indices))
        elif role == 'Troublemaker': players.append(Troublemaker(i, trblmkr_index1, trblmkr_index2))
        elif role == 'Drunk': players.append(Drunk(i, drunk_choice_index))
        elif role == 'Insomniac': players.append(Insomniac(i, insomniac_new_role))
        elif role == 'Seer': players.append(Seer(i, seer_peek_index, seer_peek_character,
                                                    seer_peek_index2, seer_peek_character2))
    return players

def wolf_init():
    ''' Initializes Wolf - gets Wolf indices and a random center card, if applicable. '''
    wolf_indices = set(find_all_player_indices('Wolf'))
    wolf_center_index, wolf_center_role = None, None
    if len(wolf_indices) == 1 and const.NUM_CENTER > 0:
        wolf_center_index = get_random_center()
        wolf_center_role = game_roles[wolf_center_index]
    logger.debug("[Hidden] Wolves are at indices: " + str(wolf_indices))
    return wolf_indices, wolf_center_index, wolf_center_role

def seer_init():
    ''' Initializes Seer - either sees 2 center cards or 1 player card. '''
    seer_index = original_roles.index('Seer')
    # TODO Change distribution of choosing center or middle cards
    choose_center = random.choice([True, False])
    if choose_center and const.NUM_CENTER > 1:
        seer_peek_index = get_random_center()
        seer_peek_character = game_roles[seer_peek_index]
        seer_peek_index2 = get_random_center()
        while seer_peek_index2 == seer_peek_index:
            seer_peek_index2 = get_random_center()
        seer_peek_character2 = game_roles[seer_peek_index2]
        logger.debug("[Hidden] Seer sees that Center " + str(seer_peek_index - const.NUM_PLAYERS) +
                " is a " + str(seer_peek_character) + " and Center " + str(seer_peek_index2 - const.NUM_PLAYERS) +
                " is a " + str(seer_peek_character2))
        return seer_peek_index, seer_peek_character, seer_peek_index2, seer_peek_character2
    else:
        seer_peek_index = get_random_player()
        while seer_peek_index == seer_index:
            seer_peek_index = get_random_player()
        seer_peek_character = game_roles[seer_peek_index]
        logger.debug("[Hidden] Seer sees that Player " + str(seer_peek_index) +
                " is a " + str(seer_peek_character))
        return seer_peek_index, seer_peek_character, None, None

def mason_init():
    ''' Initializes Mason - sees all other Masons. '''
    mason_indices = find_all_player_indices('Mason')
    logger.debug("[Hidden] Masons are at indices: " + str(mason_indices))
    return mason_indices

def robber_init():
    ''' Initializes Robber - switches roles with another player. '''
    robber_index = original_roles.index('Robber')
    robber_choice_index = get_random_player()
    while robber_choice_index == robber_index:
        robber_choice_index = get_random_player()
    robber_choice_character = game_roles[robber_choice_index]
    swap_characters(robber_index, robber_choice_index)
    logger.debug("[Hidden] Robber switches with Player " + str(robber_choice_index) +
                " and becomes a " + str(robber_choice_character))
    return robber_choice_index, robber_choice_character

def drunk_init():
    ''' Initializes Drunk - switches with a card in the center. '''
    assert(const.NUM_CENTER != 0)
    drunk_index = original_roles.index('Drunk')
    drunk_choice_index = get_random_center()
    swap_characters(drunk_index, drunk_choice_index)
    logger.debug("[Hidden] Drunk switches with Center Card " + str(drunk_choice_index - const.NUM_PLAYERS) +
                " and unknowingly becomes a " + str(game_roles[drunk_choice_index]))
    return drunk_choice_index

def troublemaker_init():
    ''' Initializes Troublemaker - switches one player with another player. '''
    troublemaker_index = original_roles.index('Troublemaker')
    troublemaker_choice_index1 = get_random_player()
    troublemaker_choice_index2 = get_random_player()
    while troublemaker_choice_index1 == troublemaker_index:
        troublemaker_choice_index1 = get_random_player()
    while troublemaker_choice_index2 == troublemaker_index or troublemaker_choice_index2 == troublemaker_choice_index1:
        troublemaker_choice_index2 = get_random_player()
    swap_characters(troublemaker_choice_index1, troublemaker_choice_index2)
    logger.debug("[Hidden] Troublemaker switches Player " + str(troublemaker_choice_index1)
        + " with Player " + str(troublemaker_choice_index2))
    return troublemaker_choice_index1, troublemaker_choice_index2

def insomniac_init(index):
    ''' Initializes Insomniac - learns new role. '''
    insomniac_new_role = game_roles[index]
    logger.debug("[Hidden] Insomniac wakes up as a " + insomniac_new_role)
    return insomniac_new_role

def swap_characters(i, j):
    ''' Util function to swap two characters, updating game_roles and the player_set. '''
    temp = game_roles[i]
    game_roles[i] = game_roles[j]
    game_roles[j] = temp
    player_set = set(game_roles[:const.NUM_PLAYERS])

def find_all_player_indices(role):
    ''' Util function to find all indices of a given role. '''
    return [i for i in range(const.NUM_PLAYERS) if game_roles[i] == role]

def get_random_player():
    ''' Gets a random player index (not in the center). '''
    return random.randint(0, const.NUM_PLAYERS - 1)

def get_random_center():
    ''' Gets a random index of a center card. '''
    return const.NUM_PLAYERS + random.randint(0, const.NUM_CENTER - 1)

def print_roles():
    logger.debug("[Hidden] Current roles: " + str(game_roles[:const.NUM_PLAYERS]) +
                "\n\t Center cards:  " + str(game_roles[const.NUM_PLAYERS:]) + '\n')

def wake(role):
    logger.info(role + ", wake up.")

def sleep(role):
    logger.info(role + ", go to sleep.\n")
