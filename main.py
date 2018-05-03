from roles import Wolf, Villager, Seer, Robber
from algorithms import baseline_solver
import random
import const

def main():

    global game_roles
    game_roles = list(const.ROLES)
    random.shuffle(game_roles)
    print("[Hidden] Initial roles: " + str(game_roles))

    ### GAME SETUP ###
    print("\n -- GAME SETUP -- \n")

    # Print out progress messages and initialize needed variables
    if 'Wolf' in const.ROLE_SET:
        wolf_indices = wolf_init()
    if 'Mason' in const.ROLE_SET:
        mason_indices = mason_init()
    if 'Seer' in const.ROLE_SET:
        seer_peek_index, seer_peek_character = seer_init()
    if 'Robber' in const.ROLE_SET:
        robber_choice_index, robber_choice_character = robber_init()

    # Initialize players
    players = []
    for i in range(const.NUM_PLAYERS):
        role = game_roles[i]
        if role == 'Wolf':
            players.append(Wolf(i, wolf_indices))
        elif role == 'Villager':
            players.append(Villager(i))
        elif role == 'Seer':
            players.append(Seer(i, seer_peek_index, seer_peek_character))
        elif role == 'Robber':
            players.append(Robber(i, robber_choice_index, robber_choice_character))
    game_roles = players
    print("[Hidden] Final roles: " + str(game_roles))

    ### GAME BEGINS ###
    print("\n -- GAME BEGINS -- \n")

    all_statements = []
    for p in players:
        all_statements.append(p.getNextStatement())

    for i in range(len(all_statements)):
        print("Player "+ str(i) + ": " + all_statements[i].sentence +
                " " + str(all_statements[i].knowledge))

    ### Make prediction ###
    n_consistent = baseline_solver(all_statements, const.NUM_PLAYERS)
    print(n_consistent)


    ### Verify prediction ###


    ### End game ###

def wolf_init():
    print("Wolves wake up.")
    wolf_indices = set()
    for i in range(const.NUM_PLAYERS):
        if game_roles[i] == 'Wolf':
            wolf_indices.add(i)
    print("[Hidden] Wolves are at indices: " + str(wolf_indices))
    print("Wolves go to sleep." + "\n")
    return wolf_indices

def seer_init():
    print("Seer wakes up.")
    seer_peek_index = random.randint(0, const.NUM_PLAYERS - 1)
    seer_peek_character = game_roles[seer_peek_index]
    print("[Hidden] Seer sees that Player " + str(seer_peek_index) +
            " is a " + str(seer_peek_character))
    print("Seer goes to sleep." + "\n")
    return seer_peek_index, seer_peek_character

def robber_init():
    print("Robber wakes up.")
    robber_index = -1
    for i in range(const.NUM_PLAYERS):
        if game_roles[i] == 'Robber':
            robber_index = i
    robber_choice_index = random.randint(0, const.NUM_PLAYERS - 1)
    while robber_choice_index == i:
        robber_choice_index = random.randint(0, const.NUM_PLAYERS - 1)
    robber_choice_character = game_roles[robber_choice_index]
    swapCharacters(robber_index, robber_choice_index)
    print("[Hidden] Robber switches with Player " + str(robber_choice_index) +
                " and becomes a " + str(robber_choice_character))
    print("Robber goes to sleep." + "\n")
    return robber_choice_index, robber_choice_character

def mason_init():
    print("Masons wake up.")
    mason_indices = set()
    for i in range(const.NUM_PLAYERS):
        if game_roles[i] == 'Mason':
            mason_indices.add(i)
    print("[Hidden] Masons are at indices: " + str(mason_indices))
    print("Masons go to sleep." + "\n")
    return mason_indices

def swapCharacters(i, j):
    temp = game_roles[i]
    game_roles[i] = game_roles[j]
    game_roles[j] = temp
    return game_roles

if __name__ == '__main__':
    main()
