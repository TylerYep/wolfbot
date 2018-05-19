from roles import *
import pickle
from algorithms import switching_solver
from predictions import makePredictions


if __name__ == '__main__':
    with open('test.pkl', 'rb') as f:
        roles, all_statements = pickle.load(f)

    logger.info("[SOLUTION] Role guesses: " + str(roles[:const.NUM_PLAYERS]) +
                "\n\t  Center cards: " + str(roles[const.NUM_PLAYERS:]) + '\n')
    print('STATEMENTS: ')
    for i, s in enumerate(all_statements):
        print(s)

    solution = switching_solver(all_statements)
    #c, d = baseline_solver(all_statments)
    print(solution)

    all_role_guesses = makePredictions(solution)
    print_guesses(all_role_guesses)
