''' main.py '''
import time

from statistics import Statistics
from one_night import play_one_night_werewolf
from algorithms import random_solver, baseline_solver, switching_solver
from const import logger
import const

def main(save_replay=True):
    ''' Simulate play_one_night_werewolf and create a Statistics instance for the runs. '''
    SOLVERS = [switching_solver]    # Solvers used in game simulations.
    start_time = time.time()
    for solver in SOLVERS:
        logger.warning('\n%s\n', solver.__name__)
        stats = Statistics()
        for num in range(const.NUM_GAMES):
            if const.SHOW_PROGRESS and num % 10 == 0:
                logger.warning('Currently on Game: %d', num)
            game_result = play_one_night_werewolf(solver, save_replay)
            stats.add_result(game_result)
        stats.print_statistics()
    logger.warning('\nTime taken: %s', str(time.time() - start_time))


if __name__ == '__main__':
    main()
