from roles import *
import pickle
from algorithms import *
from predictions import *

with open('test.pkl', 'rb') as f:
    roles, all_statments = pickle.load(f)

logger.info("[SOLUTION] Role guesses: " + str(roles[:const.NUM_PLAYERS]) +
            "\n\t  Center cards: " + str(roles[const.NUM_PLAYERS:]) + '\n')
print('STATEMENTS: ')
for i, s in enumerate(all_statments):
    print(s)

solution = switching_solver(all_statments)
#c, d = baseline_solver(all_statments)
print(solution)

all_role_guesses = makePredictions(solution)
logger.info("\n[Wolfbot] Role guesses: " + str(all_role_guesses[:const.NUM_PLAYERS]) +
            "\n\t  Center cards: " + str(all_role_guesses[const.NUM_PLAYERS:]) + '\n')
