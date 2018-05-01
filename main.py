from roles import Wolf, Villager, Seer
import random

def main():
    NUM_PLAYERS = 6
    ROLES = ('Villager', 'Villager', 'Villager', 'Wolf', 'Wolf', 'Seer')
    assignedRoles = list(ROLES)
    random.shuffle(assignedRoles)

    ### Game Setup ###

    print("Wolves wake up.")
    wolfIndices = []
    for i in range(NUM_PLAYERS):
        if assignedRoles[i] == 'Wolf':
            wolfIndices.append(i)
    print("[Hidden] Wolves are at indices: " + str(wolfIndices) + "\n")

    print("Seer wakes up.")
    seerPeekIndex = random.randint(0, NUM_PLAYERS - 1)
    seerPeekCharacter = assignedRoles[seerPeekIndex]
    print("[Hidden] Seer sees that Player " + str(seerPeekIndex) + " is a " + str(seerPeekCharacter) + "\n")

    ### Game Begins ###

    print("GAME BEGINS")
    players = []
    for i in range(NUM_PLAYERS):
        if assignedRoles[i] == 'Wolf':
            players.append(Wolf(i, wolfIndices))
        elif assignedRoles[i] == 'Villager':
            players.append(Villager(i))
        elif assignedRoles[i] == 'Seer':
            players.append(Seer(i, seerPeekIndex, seerPeekCharacter))
    print(players)
    print('\n')

    all_statements = []
    for p in players:
        all_statements.append(p.getNextStatement())
    for p in all_statements:
        print(p)

    # Make prediction
    baseline_solver(all_statements, NUM_PLAYERS)
    # Verify prediction
    # End game

if __name__ == '__main__':
    main()
