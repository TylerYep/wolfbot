from roles import Wolf, Villager, Seer, Robber, Mason
import random
import const
from const import logger

def play_one_night_werewolf(solver):
    global game_roles, player_set
    game_roles = list(const.ROLES)
    random.shuffle(game_roles)
    player_set = set(game_roles[:const.NUM_PLAYERS])

    print_roles()
    player_objs = night_falls()
    print_roles()

    logger.info("\n -- GAME BEGINS -- \n")
    all_statements = getStatements(player_objs)
    consistent_statements = solver(all_statements)
    # print(consistent_statements)
    wolf_suspects = makePredictions(consistent_statements)
    return verifyPredictions(wolf_suspects)
    ### End game ###

def verifyPredictions(wolf_suspects):
    correctGuesses = 0
    totalWolves = 0
    for w in wolf_suspects:
        if game_roles[w] == 'Wolf':
            correctGuesses += 1
    for card in game_roles[:const.NUM_PLAYERS]:
        if card == 'Wolf':
            totalWolves += 1
    return correctGuesses, totalWolves, correctGuesses >= 1, correctGuesses == totalWolves

def makePredictions(consistent_statements):
    wolf_suspects, all_suspects = [], []
    for j in range(len(consistent_statements)):
        if not consistent_statements[j]:
            wolf_suspects.append(j)
            all_suspects.append('Wolf')
            logger.info("I suspect Player " + str(j) + " is a Wolf!")
        else:
            # TODO make it guess the remaining roles
            all_suspects.append("")
    return wolf_suspects

def getStatements(player_objs):
    all_statements = []
    for j in range(const.NUM_PLAYERS):
        all_statements.append(player_objs[j].getNextStatement())
        logger.info("Player " + str(j) + ": " + all_statements[j].sentence +
                " " + str(all_statements[j].knowledge))
    return all_statements

# Print out progress messages and initialize needed variables
def night_falls():
    logger.info("\n -- NIGHT FALLS -- \n")
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
        seer_peek_index, seer_peek_character = seer_init()
    sleep('Seer')
    wake('Robber')
    if 'Robber' in player_set:
        robber_choice_index, robber_choice_character = robber_init()
    sleep('Robber')
    # wake(Troublemaker)
    # if 'Troublemaker' in player_set:
    #     trblmkr_choice_index1, trblmkr_choice_index2 = trblmkr_init()
    # sleep(Troublemaker)
    # wake('Drunk')
    # if 'Drunk' in player_set:
    #     drunk_choice_index, drunk_choice_character = drunk_init()
    # sleep('Drunk')
    # wake('Insomniac')
    # if 'Insomniac' in player_set:
    #     insomniac_new_role = insomniac_init()
    # sleep('Insomniac')

    # Initialize players
    players = []
    for i in range(const.NUM_ROLES):
        if i >= const.NUM_PLAYERS:
            players.append(game_roles[i])
        else:
            role = game_roles[i]
            if role == 'Wolf': players.append(Wolf(i, wolf_indices))
            elif role == 'Villager': players.append(Villager(i))
            elif role == 'Seer': players.append(Seer(i, seer_peek_index, seer_peek_character))
            elif role == 'Robber': players.append(Robber(i, robber_choice_index, robber_choice_character))
            elif role == 'Mason': players.append(Mason(i, mason_indices))
            elif role == 'Troublemaker': players.append("")
            elif role == 'Drunk': players.append("")
            elif role == 'Insomniac': players.append("")
    return players

# TODO Wolf can look at card in center
def wolf_init():
    wolf_indices = set()
    for i in range(const.NUM_PLAYERS):
        if game_roles[i] == 'Wolf':
            wolf_indices.add(i)
    logger.debug("[Hidden] Wolves are at indices: " + str(wolf_indices))
    return wolf_indices

# TODO Seer can look at two center cards
def seer_init():
    seer_peek_index = random.randint(0, const.NUM_PLAYERS - 1)
    seer_peek_character = game_roles[seer_peek_index]
    logger.debug("[Hidden] Seer sees that Player " + str(seer_peek_index) +
            " is a " + str(seer_peek_character))
    return seer_peek_index, seer_peek_character

def mason_init():
    mason_indices = []
    for i in range(const.NUM_PLAYERS):
        if game_roles[i] == 'Mason':
            mason_indices.append(i)
    logger.debug("[Hidden] Masons are at indices: " + str(mason_indices))
    return mason_indices

def robber_init():
    robber_index = -1
    for i in range(const.NUM_PLAYERS):
        if game_roles[i] == 'Robber':
            robber_index = i
    robber_choice_index = random.randint(0, const.NUM_PLAYERS - 1)
    while robber_choice_index == i:
        robber_choice_index = random.randint(0, const.NUM_PLAYERS - 1)
    robber_choice_character = game_roles[robber_choice_index]
    swapCharacters(robber_index, robber_choice_index)
    logger.debug("[Hidden] Robber switches with Player " + str(robber_choice_index) +
                " and becomes a " + str(robber_choice_character))
    return robber_choice_index, robber_choice_character

def drunk_init():
    drunk_index = -1
    for i in range(const.NUM_PLAYERS):
        if game_roles[i] == 'Drunk':
            drunk_index = i
    drunk_choice_index = const.NUM_PLAYERS + random.randint(0, const.NUM_CENTER - 1)
    # Unknown to the Drunk player
    drunk_choice_character = game_roles[drunk_choice_index]
    swapCharacters(drunk_index, drunk_choice_index)
    logger.debug("[Hidden] Drunk switches with Center Card " + str(drunk_choice_index) +
                " and becomes a " + str(drunk_choice_character))
    return drunk_choice_index, drunk_choice_character

def swapCharacters(i, j):
    temp = game_roles[i]
    game_roles[i] = game_roles[j]
    game_roles[j] = temp
    player_set = set(game_roles[:const.NUM_PLAYERS])

def print_roles():
    logger.debug("[Hidden] Current roles: " + str(game_roles[:const.NUM_PLAYERS]) +
                "\n\t Center cards:  " + str(game_roles[const.NUM_PLAYERS:]) + '\n')

def wake(role):
    logger.info(role + ", wake up.")

def sleep(role):
    logger.info(role + ", go to sleep.\n")
