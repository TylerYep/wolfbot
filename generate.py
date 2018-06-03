import sys
if sys.version_info < (3, 0): sys.stdout.write("\n\n Requires Python 3, not Python 2! \n\n\n")
from one_night import play_one_night_werewolf
from algorithms import random_solver, baseline_solver, switching_solver
from statistics import GameResult, Statistics
from const import logger
import const
import time
import pickle

def generate_data(n_sim=1):
    #weights = [3**i for i in range(1, const.NUM_PLAYERS+1)]
    #sim_list = []
    #logger.setLevel(30)
    #for i, w in enumerate(weights):
    #    const.FIXED_WOLF_INDEX = i
    #    print(i)
    #    for _ in range(w):
    #        #if i % 1000 == 0: print('Simulation: ', i)
    #        simulation = play_one_night_werewolf(switching_solver)
    #        sim_list.append(simulation)
    sim_list = []
    logger.setLevel(30)
    for i in range(n_sim):
        if i % 1000 == 0: print('Simulation: ', i)
        simulation = play_one_night_werewolf(switching_solver)
        sim_list.append(simulation)

    fname = 'data_small/simulation_' + time.strftime("%Y%m%d_%H%M%S") + '.pkl'
    with open(fname, 'wb') as f: pickle.dump(sim_list, f)

if __name__ == '__main__':
    generate_data(100000)
#    for i in range(1000): 
#        try:
#            generate_data(1000)
#            print('Just finished batch:', i)
#        except:
#            print('something went wrong')
