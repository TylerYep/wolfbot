from one_night import play_one_night_werewolf
from algorithms import baseline_solver, random_solver, switching_solver
import const
from const import logger

def main():
    correct, total = 0.0, 0.0
    match1, match2 = 0.0, 0.0
    for _ in range(const.NUM_GAMES):
        c, t, s1, s2 = play_one_night_werewolf(switching_solver)
        correct += c
        total += t
        if s1: match1 += 1
        if s2: match2 += 1
    if total == 0.0: total += 1
    logger.warning("S1: Found at least 1 Wolf: " + str(match1 / const.NUM_GAMES))
    logger.warning("S2: Found all Wolves: " + str(match2 / const.NUM_GAMES))
    logger.warning("Correct guesses (not accusing extraneous wolves): " + str(correct / total))

if __name__ == '__main__':
    main()
