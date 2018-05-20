import sys
if sys.version_info < (3, 0): sys.stdout.write("\n\nRequires Python 3, not Python 2!\n\n\n")
from one_night import play_one_night_werewolf
from algorithms import baseline_solver, random_solver, switching_solver
import const
from const import logger

def main():
    correct1, total1 = 0.0, 0.0
    correct2, total2 = 0.0, 0.0
    match1, match2 = 0.0, 0.0
    for _ in range(const.NUM_GAMES):
        game_roles, all_role_guesses = play_one_night_werewolf(switching_solver)
        c, t = correctness_strict(game_roles, all_role_guesses)
        correct1 += c
        total1 += t
        c2, t2 = verify_predictions(game_roles, all_role_guesses)
        correct2 += c2
        total2 += t2
        if c2 >= 1: match1 += 1 # Found at least 1 Wolf
        if c2 == t2: match2 += 1 # Found all wolves

    if total1 == 0.0: total1 += 1
    if total2 == 0.0: total2 += 1
    logger.warning("Accuracy for all predictions: " + str(correct1 / total1))
    logger.warning("S1: Found at least 1 Wolf: " + str(match1 / const.NUM_GAMES))
    logger.warning("S2: Found all Wolves: " + str(match2 / const.NUM_GAMES))
    logger.warning("Correct guesses (not accusing extraneous wolves): " + str(correct2 / total2))

# Returns fraction of how many roles were guessed correctly out of all roles.
def correctness_strict(game_roles, all_role_guesses):
    correct, total = 0.0, 0.0
    for i in range(const.NUM_ROLES):
        total += 1
        if game_roles[i] == all_role_guesses[i]:
            correct += 1
    return correct, total

# Returns fraction of how many player roles were guessed correctly.
# Optionally adds a bonus for a matching center set. (Bonus only applies when center is identical)
def correctness_lenient_center(game_roles, all_role_guesses, use_center=False):
    correct, total = 0.0, 0.0
    for i in range(const.NUM_PLAYERS):
        total += 1
        if game_roles[i] == all_role_guesses[i]:
            correct += 1
    center_set = set(game_roles[const.NUM_PLAYERS:])
    center_set2 = set(all_role_guesses[const.NUM_PLAYERS:])
    if use_center:
        if center_set == center_set2:
            correct += const.NUM_CENTER
            total += const.NUM_CENTER
    return correct, total

# Returns fraction of how many Wolves were correctly identified.
# Only counts Wolves that are players.
def verify_predictions(game_roles, all_role_guesses):
    correctGuesses = 0
    totalWolves = 0
    for r in range(const.NUM_ROLES):
        if game_roles[r] == 'Wolf' == all_role_guesses[r]:
            correctGuesses += 1
    for card in game_roles[:const.NUM_PLAYERS]:
        if card == 'Wolf':
            totalWolves += 1
    return correctGuesses, totalWolves

if __name__ == '__main__':
    main()
