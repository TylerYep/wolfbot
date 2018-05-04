from one_night import play_one_night_werewolf
import const
from const import logger

def main():
    correct, total = 0.0, 0.0
    match1, match2 = 0.0, 0.0
    for _ in range(const.NUM_GAMES):
        c, t, s1, s2 = play_one_night_werewolf()
        correct += c
        total += t
        if s1: match1 += 1
        if s2: match2 += 1
    if total == 0.0: total += 1
    logger.warning("S1 perfect: " + str(match1/total))
    logger.warning("S2 perfect: " + str(match2/total))
    logger.warning("Percentage correct: " + str(correct/total))

if __name__ == '__main__':
    main()
