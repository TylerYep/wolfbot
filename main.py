import sys
if sys.version_info < (3, 0): sys.stdout.write("\n\nRequires Python 3, not Python 2!\n\n\n")
from one_night import play_one_night_werewolf
from algorithms import baseline_solver, random_solver, switching_solver
import const
from const import logger

def main():
    correct, total = 0.0, 0.0
    match1, match2 = 0.0, 0.0
    for _ in range(const.NUM_GAMES):
        game_roles, all_role_guesses = play_one_night_werewolf(switching_solver)
        c, t, s1, s2 = verify_predictions(game_roles, all_role_guesses)
        correct += c
        total += t
        if s1: match1 += 1
        if s2: match2 += 1
    if total == 0.0: total += 1
    logger.warning("S1: Found at least 1 Wolf: " + str(match1 / const.NUM_GAMES))
    logger.warning("S2: Found all Wolves: " + str(match2 / const.NUM_GAMES))
    logger.warning("Correct guesses (not accusing extraneous wolves): " + str(correct / total))

def verify_predictions(game_roles, all_role_guesses):
    correctGuesses = 0
    totalWolves = 0
    for r in range(len(all_role_guesses)):
        if game_roles[r] == 'Wolf' == all_role_guesses[r]:
            correctGuesses += 1
    for card in game_roles[:const.NUM_PLAYERS]:
        if card == 'Wolf':
            totalWolves += 1
    return correctGuesses, totalWolves, correctGuesses >= 1, correctGuesses == totalWolves

if __name__ == '__main__':
    main()
