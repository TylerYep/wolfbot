import sys
if sys.version_info < (3, 0): sys.stdout.write('\n\n Requires Python 3, not Python 2! \n\n\n')
from one_night import play_one_night_werewolf
from algorithms import random_solver, baseline_solver, switching_solver
from statistics import GameResult, Statistics
from const import logger
from encoder import WolfBotEncoder
import const
import time
import json

def generate_data(n_sim=1):
    weights = [3]
    sim_list = []
    logger.setLevel(30)
    for i, w in enumerate(weights):
        const.FIXED_WOLF_INDEX = i
        logger.warning('Computing index: ' + str(i))
        for _ in range(w):
            simulation = play_one_night_werewolf(switching_solver)
            sim_list.append(simulation)

    fname = 'data/simulations/simulation_' + time.strftime('%Y%m%d_%H%M%S') + '.json'
    with open(fname, 'w') as f: json.dump(sim_list, f, cls=WolfBotEncoder)

if __name__ == '__main__':
    generate_data()
