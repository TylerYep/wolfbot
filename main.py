from roles import Wolf, Villager, Seer
from algorithms import baseline_solver
import random
import const

def main():

    ### Game Setup ###

    assigned_roles = list(const.ROLES)
    random.shuffle(assigned_roles)

    print("Wolves wake up.")
    wolf_indices = set()
    for i in range(const.NUM_PLAYERS):
        if assigned_roles[i] == 'Wolf':
            wolf_indices.add(i)
    print("[Hidden] Wolves are at indices: " + str(wolf_indices) + "\n")

    print("Seer wakes up.")
    seer_peek_index = random.randint(0, const.NUM_PLAYERS - 1)
    seer_peek_character = assigned_roles[seer_peek_index]
    print("[Hidden] Seer sees that Player " + str(seer_peek_index) + " is a " + str(seer_peek_character) + "\n")

    ### Game Begins ###

    print("GAME BEGINS")
    players = []
    for i in range(const.NUM_PLAYERS):
        if assigned_roles[i] == 'Wolf':
            players.append(Wolf(i, wolf_indices))
        elif assigned_roles[i] == 'Villager':
            players.append(Villager(i))
        elif assigned_roles[i] == 'Seer':
            players.append(Seer(i, seer_peek_index, seer_peek_character))
    print("[Hidden] " + str(players))

    all_statements = []
    for p in players:
        all_statements.append(p.getNextStatement())

    for i in range(len(all_statements)):
        print("Player "+ str(i) + ": " + all_statements[i].sentence + " " + str(all_statements[i].knowledge))

    # Make prediction
    # baseline_solver(all_statements, NUM_PLAYERS)

    # Verify prediction
    # End game

if __name__ == '__main__':
    main()
