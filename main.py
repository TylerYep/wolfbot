from roles import Wolf, Villager, Seer, Robber, Mason
from algorithms import baseline_solver
import random
import const
from const import logger

def main():
    correct, total = 0.0, 0.0
    for _ in range(const.NUM_GAMES):
        correct += play_one_night_werewolf()
        total += const.ROLE_COUNTS['Wolf']
    logger.warning("Percentage correct: " + str(correct/total))

def print_roles():
    logger.info("[Hidden] Current roles: " + str(game_roles) + '\n')

def play_one_night_werewolf():
    ### GAME SETUP ###
    logger.info("\n -- NIGHT FALLS -- \n")

    global game_roles
    game_roles = list(const.ROLES)
    random.shuffle(game_roles)

    print_roles()
    game_roles = night_falls()
    print_roles()

    ### GAME BEGINS ###

    # Only get statements from players
    all_statements = []
    for j in range(const.NUM_PLAYERS):
        player = game_roles[j]
        all_statements.append(player.getNextStatement())

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
    for w in wolf_suspects:
        if game_roles[w].role == 'Wolf':
            correctGuesses += 1
    return correctGuesses

    ### End game ###

# Print out progress messages and initialize needed variables
def night_falls():
    if 'Wolf' in const.ROLE_SET:
        wolf_indices = wolf_init()
    # if 'Minion' in const.ROLE_SET:
    #     logger.info('')
    if 'Mason' in const.ROLE_SET:
        mason_indices = mason_init()
    if 'Seer' in const.ROLE_SET:
        seer_peek_index, seer_peek_character = seer_init()
    if 'Robber' in const.ROLE_SET:
        robber_choice_index, robber_choice_character = robber_init()
    if 'Troublemaker' in const.ROLE_SET:
        logger.info('')
    if 'Drunk' in const.ROLE_SET:
        logger.info('')
    # if 'Insomniac' in const.ROLE_SET:
    #     logger.info('')

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
    return players

# TODO Wolf can look at card in center
def wolf_init():
    logger.info("Wolves wake up.")
    wolf_indices = set()
    for i in range(const.NUM_PLAYERS):
        if game_roles[i] == 'Wolf':
            wolf_indices.add(i)
    logger.info("[Hidden] Wolves are at indices: " + str(wolf_indices))
    logger.info("Wolves go to sleep." + "\n")
    return wolf_indices

# TODO Seer can look at two center cards
def seer_init():
    logger.info("Seer wakes up.")
    seer_peek_index = random.randint(0, const.NUM_PLAYERS - 1)
    seer_peek_character = game_roles[seer_peek_index]
    logger.info("[Hidden] Seer sees that Player " + str(seer_peek_index) +
            " is a " + str(seer_peek_character))
    logger.info("Seer goes to sleep." + "\n")
    return seer_peek_index, seer_peek_character

def robber_init():
    logger.info("Robber wakes up.")
    robber_index = -1
    for i in range(const.NUM_PLAYERS):
        if game_roles[i] == 'Robber':
            robber_index = i
    robber_choice_index = random.randint(0, const.NUM_PLAYERS - 1)
    while robber_choice_index == i:
        robber_choice_index = random.randint(0, const.NUM_PLAYERS - 1)
    robber_choice_character = game_roles[robber_choice_index]
    swapCharacters(robber_index, robber_choice_index)
    logger.info("[Hidden] Robber switches with Player " + str(robber_choice_index) +
                " and becomes a " + str(robber_choice_character))
    logger.info("Robber goes to sleep." + "\n")
    return robber_choice_index, robber_choice_character

def mason_init():
    logger.info("Masons wake up.")
    mason_indices = []
    for i in range(const.NUM_PLAYERS):
        if game_roles[i] == 'Mason':
            mason_indices.append(i)
    logger.info("[Hidden] Masons are at indices: " + str(mason_indices))
    logger.info("Masons go to sleep." + "\n")
    return mason_indices

def swapCharacters(i, j):
    temp = game_roles[i]
    game_roles[i] = game_roles[j]
    game_roles[j] = temp
    return game_roles

if __name__ == '__main__':
    main()
