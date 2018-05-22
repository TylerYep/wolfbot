import sys
if sys.version_info < (3, 0): sys.stdout.write("\n\nRequires Python 3, not Python 2!\n\n\n")
from one_night import play_one_night_werewolf
from algorithms import random_solver, baseline_solver, switching_solver
import const
from const import logger

def main():
    metrics = [correctness_strict, correctness_lenient_center, verify_predictions]
    NUM_METRICS = len(metrics)
    correct = [0.0 for _ in range(NUM_METRICS)]
    total = [0.0 for _ in range(NUM_METRICS)]
    match1, match2 = 0.0, 0.0

    for num in range(const.NUM_GAMES):
        game_roles, all_role_guesses = play_one_night_werewolf(switching_solver)
        if num % 10 == 0 and const.NUM_GAMES > 10: logger.warning(str(num))
        
        for i in range(NUM_METRICS):
            c, t = metrics[i](game_roles, all_role_guesses)
            correct[i] += c
            total[i] += t
            if c >= 1 and i == 2: match1 += 1 # Found at least 1 Wolf
            if c == t and i == 2: match2 += 1 # Found two player wolves
    for t in total:
        if t == 0: t += 1
    logger.warning("Accuracy for all predictions: " + str(correct[0] / total[0]))
    logger.warning("Accuracy with lenient center scores: " + str(correct[1] / total[1]))
    logger.warning("S1: Found at least 1 Wolf: " + str(match1 / const.NUM_GAMES))
    logger.warning("S2: Found two player Wolves: " + str(match2 / const.NUM_GAMES))
    logger.warning("Correct guesses (not accusing extraneous wolves): " + str(correct[2] / total[2]))

# Returns fraction of how many roles were guessed correctly out of all roles.
def correctness_strict(game_roles, all_role_guesses):
    correct, total = 0.0, 0.0
    for i in range(const.NUM_ROLES):
        total += 1
        if game_roles[i] == all_role_guesses[i]:
            correct += 1
    return correct, total

# Returns fraction of how many player roles were guessed correctly.
# Optionally adds a bonus for a matching center set.
def correctness_lenient_center(game_roles, all_role_guesses):
    correct, total = 0.0, 0.0
    for i in range(const.NUM_PLAYERS):
        total += 1
        if game_roles[i] == all_role_guesses[i]:
            correct += 1
    center_set = set(game_roles[const.NUM_PLAYERS:])
    center_set2 = set(all_role_guesses[const.NUM_PLAYERS:])
    # TODO fix this please
    correct += len(center_set & center_set2)
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
