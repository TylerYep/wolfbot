from one_night import play_one_night_werewolf
import const
from const import logger

def main():
    correct, total = 0.0, 0.0
    for _ in range(const.NUM_GAMES):
        c, t = play_one_night_werewolf()
        correct += c
        total += t
    if total == 0.0: total += 1
    logger.warning("Percentage correct: " + str(correct/total))

if __name__ == '__main__':
    main()
