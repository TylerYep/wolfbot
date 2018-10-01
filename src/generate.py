''' generate.py '''
import time
import json

from algorithms import switching_solver
from encoder import WolfBotEncoder
from one_night import play_one_night_werewolf
from const import logger
import const

def generate_data():
    ''' Simulate games and store data in simulations folder. '''
    weights = [3**i for i in range(1, const.NUM_PLAYERS + 1)]
    sim_list = []
    logger.setLevel(0)
    for i, weight in enumerate(weights):
        const.FIXED_WOLF_INDEX = i
        logger.warning('Computing index: %d', i)
        for _ in range(weight):
            simulation = play_one_night_werewolf(switching_solver)
            sim_list.append(simulation)

    fname = 'data/simulations/simulation_' + time.strftime('%Y%m%d_%H%M%S') + '.json'
    with open(fname, 'w') as f_sim:
        json.dump(sim_list, f_sim, cls=WolfBotEncoder)

if __name__ == '__main__':
    generate_data()
