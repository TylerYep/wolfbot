from roles import Wolf, Villager, Seer, Robber, Mason
from algorithms import baseline_solver
import random
import const
from const import logger

def print_roles():
    logger.debug("[Hidden] Current roles: " + str(game_roles[:const.NUM_PLAYERS]) +
                "\n\t Center cards:  " + str(game_roles[const.NUM_PLAYERS:]) + '\n')

def play_one_night_werewolf():
    ### GAME SETUP ###
    logger.info("\n -- NIGHT FALLS -- \n")

    global game_roles, game_set
    game_roles = list(const.ROLES)
    random.shuffle(game_roles)
    game_set = set(game_roles[:const.NUM_PLAYERS])

    print_roles()
    game_roles = night_falls()
    print_roles()

    ### GAME BEGINS ###

    all_statements = []
    for j in range(const.NUM_PLAYERS):
        all_statements.append(game_roles[j].getNextStatement())

    logger.info("\n -- GAME BEGINS -- \n")
    for i in range(len(all_statements)):
        logger.info("Player "+ str(i) + ": " + all_statements[i].sentence +
                " " + str(all_statements[i].knowledge))

    ### Make prediction ###
    consistent_statements = baseline_solver(all_statements)
    wolf_suspects = []
    for j in range(len(consistent_statements)):
        if not consistent_statements[j]:
            wolf_suspects.append(j)
            logger.info("I suspect Player " + str(j) + " is a Wolf!")

    ### Verify prediction ###
    correctGuesses = 0
    totalWolves = 0
    for w in wolf_suspects:
        if game_roles[w].role == 'Wolf':
            correctGuesses += 1
    for card in game_roles[:const.NUM_PLAYERS]:
        if card.role == 'Wolf':
            totalWolves += 1
    return correctGuesses, totalWolves, correctGuesses >= 1, correctGuesses == totalWolves

    ### End game ###

# Print out progress messages and initialize needed variables
def night_falls():
    logger.info("Wolves wake up.")
    if 'Wolf' in game_set:
        wolf_indices = wolf_init()
    logger.info("Wolves go to sleep.\n")
    logger.info("Masons wake up.")
    if 'Mason' in game_set:
        mason_indices = mason_init()
    logger.info("Masons go to sleep.\n")
    logger.info("Seer wakes up.")
    if 'Seer' in game_set:
        seer_peek_index, seer_peek_character = seer_init()
    logger.info("Seer goes to sleep.\n")
    # logger.info("Robber wakes up.")
    # if 'Robber' in game_set:
    #     robber_choice_index, robber_choice_character = robber_init()
    # logger.info("Robber goes to sleep.\n")
    # logger.info("Troublemaker wakes up.")
    # if 'Troublemaker' in game_set:
    #     res = trblmkr_init()
    #     trblmkr_choice_index1, trblmkr_choice_character1 = res[0]
    #     trblmkr_choice_index2, trblmkr_choice_character2 = res[1]
    # logger.info("Troublemaker goes to sleep.\n")
    # logger.info("Drunk wakes up.")
    # if 'Drunk' in game_set:
    #     drunk_choice_index, drunk_choice_character = drunk_init()
    # logger.info("Drunk goes to sleep.\n")
    # logger.info("Insomniac wakes up.")
    # if 'Insomniac' in game_set:
    #     insomniac_new_role = insomniac_init()
    # logger.info("Insomniac goes to sleep.\n")

    # Initialize players
    players = []
    for i in range(const.NUM_ROLES):
        if i >= const.NUM_PLAYERS:
            players.append(game_roles[i])
        else:
            role = game_roles[i]
            if role == 'Wolf':
                players.append(Wolf(i, wolf_indices))
            elif role == 'Villager':
                players.append(Villager(i))
            elif role == 'Seer':
                players.append(Seer(i, seer_peek_index, seer_peek_character))
            elif role == 'Robber':
                players.append(Robber(i, robber_choice_index, robber_choice_character))
            elif role == 'Mason':
                players.append(Mason(i, mason_indices))
            elif role == 'Troublemaker':
                players.append("")
            elif role == 'Drunk':
                players.append("")
            elif role == 'Insomniac':
                players.append("")
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

def swapCharacters(i, j):
    temp = game_roles[i]
    game_roles[i] = game_roles[j]
    game_roles[j] = temp
    game_set = set(game_roles[:const.NUM_PLAYERS])
