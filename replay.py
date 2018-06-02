from const import logger
import const
import pickle
from algorithms import switching_solver
from predictions import make_predictions, print_guesses

if __name__ == '__main__':
    with open('replay.pkl', 'rb') as f:
        original_roles, roles, all_statements = pickle.load(f)

    print('STATEMENTS: ')
    for i, s in enumerate(all_statements):
        print(s)

    logger.warning("[Hidden] Current roles: " + str(original_roles[:const.NUM_PLAYERS]) +
            "\n\t Center cards:  " + str(original_roles[const.NUM_PLAYERS:]) + '\n')
    logger.warning("[SOLUTION] Role guesses: " + str(roles[:const.NUM_PLAYERS]) +
                "\n\t  Center cards: " + str(roles[const.NUM_PLAYERS:]) + '\n')

    solution = switching_solver(all_statements)
    logger.warning(solution)

    all_role_guesses = make_predictions(solution)
    print_guesses(all_role_guesses)
