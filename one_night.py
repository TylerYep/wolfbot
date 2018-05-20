from roles import Villager, Wolf, Mason, Seer, Robber, Troublemaker, Drunk, Insomniac
from predictions import make_predictions, print_guesses, verify_predictions
from const import logger
import const
import pickle
import random
from possible import get_possible_statements

def play_one_night_werewolf(solver):
    global game_roles, original_roles, player_set
    game_roles = list(const.ROLES)
    random.shuffle(game_roles)
    player_set = set(game_roles[:const.NUM_PLAYERS])
    original_roles = list(game_roles)

    print_roles()
    player_objs = night_falls()

    logger.info("\n -- GAME BEGINS -- \n")
    possib = get_possible_statements(const.ROLE_SET)
    all_statements = getStatements(player_objs, possib)
    print_roles()
    game = [game_roles, all_statements]
    with open('test.pkl', 'wb') as f: pickle.dump(game, f)

    solution = solver(all_statements)
    logger.info("Solver interpretation: " + str(solution.path))
    all_role_guesses = make_predictions(solution)
    print_guesses(all_role_guesses)

    return verify_predictions(game_roles, all_role_guesses)

def getStatements(player_objs, possib):
    all_statements = []
    for j in range(const.NUM_PLAYERS):
        statement = player_objs[j].getNextStatement(all_statements, possib)
        all_statements.append(statement)
        logger.info("Player " + str(j) + ": " + str(all_statements[j].sentence))
    return all_statements

# Print out progress messages and initialize needed variables
def night_falls():
    logger.info("\n -- NIGHT FALLS -- \n")
    insomniac_ind = find_role_index('Insomniac')
    wake('Wolves')
    if 'Wolf' in player_set:
        wolf_indices = wolf_init()
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
        new_insomniac_index, insomniac_new_role = insomniac_init(insomniac_ind)
    sleep('Insomniac')

    # Initialize players
    players = []
    for i in range(const.NUM_ROLES):
        if i >= const.NUM_PLAYERS:      # Center cards
            players.append(original_roles[i])
        else:
            role = original_roles[i]
            if role == 'Wolf': players.append(Wolf(i, wolf_indices))
            elif role == 'Villager': players.append(Villager(i))
            elif role == 'Seer': players.append(Seer(i, seer_peek_index, seer_peek_character, seer_peek_index2, seer_peek_character2))
            elif role == 'Robber': players.append(Robber(i, robber_choice_index, robber_choice_character))
            elif role == 'Mason': players.append(Mason(i, mason_indices))
            elif role == 'Troublemaker': players.append(Troublemaker(i, trblmkr_index1, trblmkr_index2))
            elif role == 'Drunk': players.append(Drunk(i, drunk_choice_index))
            elif role == 'Insomniac': players.append(Insomniac(i, new_insomniac_index, insomniac_new_role))
    return players

# TODO Wolf can look at card in center
def wolf_init():
    wolf_indices = set()
    for i in range(const.NUM_PLAYERS):
        if game_roles[i] == 'Wolf':
            wolf_indices.add(i)
    logger.debug("[Hidden] Wolves are at indices: " + str(wolf_indices))
    return wolf_indices

def seer_init():
    seer_index = find_role_index('Seer')
    choose_center = random.choice([True, False]) # Choose distribution of choosing center or middle cards
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
    mason_indices = []
    for i in range(const.NUM_PLAYERS):
        if game_roles[i] == 'Mason':
            mason_indices.append(i)
    logger.debug("[Hidden] Masons are at indices: " + str(mason_indices))
    return mason_indices

def robber_init():
    robber_index = find_role_index('Robber')
    robber_choice_index = get_random_player()
    while robber_choice_index == robber_index:
        robber_choice_index = get_random_player()
    robber_choice_character = game_roles[robber_choice_index]
    swapCharacters(robber_index, robber_choice_index)
    logger.debug("[Hidden] Robber switches with Player " + str(robber_choice_index) +
                " and becomes a " + str(robber_choice_character))
    return robber_choice_index, robber_choice_character

def drunk_init():
    drunk_index = find_role_index('Drunk')
    assert(const.NUM_CENTER != 0)
    drunk_choice_index = get_random_center()
    swapCharacters(drunk_index, drunk_choice_index)
    logger.debug("[Hidden] Drunk switches with Center Card " + str(drunk_choice_index - const.NUM_PLAYERS) +
                " and unknowingly becomes a " + str(game_roles[drunk_choice_index]))
    return drunk_choice_index

def troublemaker_init():
    troublemaker_index = find_role_index('Troublemaker')
    troublemaker_choice_index1 = get_random_player()
    troublemaker_choice_index2 = get_random_player()
    while troublemaker_choice_index1 == troublemaker_index:
        troublemaker_choice_index1 = get_random_player()
    while troublemaker_choice_index2 == troublemaker_index or troublemaker_choice_index2 == troublemaker_choice_index1:
        troublemaker_choice_index2 = get_random_player()
    swapCharacters(troublemaker_choice_index1, troublemaker_choice_index2)
    logger.debug("[Hidden] Troublemaker switches Player " + str(troublemaker_choice_index1)
        + " with Player " + str(troublemaker_choice_index2))
    return troublemaker_choice_index1, troublemaker_choice_index2

def insomniac_init(index):
    new_insomniac_index = find_role_index('Insomniac')
    insomniac_new_role = game_roles[index]
    return new_insomniac_index, insomniac_new_role

def swapCharacters(i, j):
    temp = game_roles[i]
    game_roles[i] = game_roles[j]
    game_roles[j] = temp
    player_set = set(game_roles[:const.NUM_PLAYERS])

def find_role_index(role):
    for i in range(const.NUM_PLAYERS):
        if original_roles[i] == role:
            return i
    return -1

def get_random_player():
    return random.randint(0, const.NUM_PLAYERS - 1)

def get_random_center():
    return const.NUM_PLAYERS + random.randint(0, const.NUM_CENTER - 1)

def print_roles():
    logger.debug("[Hidden] Current roles: " + str(game_roles[:const.NUM_PLAYERS]) +
                "\n\t Center cards:  " + str(game_roles[const.NUM_PLAYERS:]) + '\n')

def wake(role):
    logger.info(role + ", wake up.")

def sleep(role):
    logger.info(role + ", go to sleep.\n")
