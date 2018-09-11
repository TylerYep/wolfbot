import sys
if sys.version_info < (3, 0): sys.stdout.write('\n\n Requires Python 3, not Python 2! \n\n\n')
from one_night import play_one_night_werewolf
from algorithms import random_solver, baseline_solver, switching_solver
from statistics import GameResult, Statistics
from const import logger
import const
import time
import pickle

def main():
    # Initialize array of solvers used in game simulations.
    SOLVERS = [switching_solver]
    start_time = time.time()
    for solver in SOLVERS:
        logger.warning('\n' + solver.__name__ + '\n')
        stats = Statistics()
        for num in range(const.NUM_GAMES):
            if const.SHOW_PROGRESS and num % 10 == 0:
                logger.warning('Currently on Game: ' + str(num))
            game_result = play_one_night_werewolf(solver)
            stats.add_result(game_result)
        stats.print_statistics()
    logger.warning('Time taken: ' + str(time.time() - start_time))

if __name__ == '__main__': main()
