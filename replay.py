from const import logger
import const
import pickle
from algorithms import switching_solver
from predictions import make_predictions, print_guesses
from statistics import Statistics, GameResult

if __name__ == '__main__':
    with open('predictions.pkl', 'rb') as f:
        solution, all_role_guesses, curr_role_counts = pickle.load(f)

    print(solution)
    print(all_role_guesses)
    print(curr_role_counts)




    # with open('replay.pkl', 'rb') as f:
    #    original_roles, game_roles, all_statements = pickle.load(f)

    # print('STATEMENTS: ')
    # for i, s in enumerate(all_statements):
    #     print(s)
    #
    # logger.warning("[Hidden] Current roles: " + str(original_roles[:const.NUM_PLAYERS]) +
    #         "\n\t Center cards:  " + str(original_roles[const.NUM_PLAYERS:]) + '\n')
    # logger.warning("[SOLUTION] Role guesses: " + str(game_roles[:const.NUM_PLAYERS]) +
    #             "\n\t  Center cards: " + str(game_roles[const.NUM_PLAYERS:]) + '\n')
    #
    # solution = switching_solver(all_statements)
    # logger.warning(solution)
    #
    # all_role_guesses = make_predictions(solution)
    # print_guesses(all_role_guesses)
    #
    # game_result = GameResult(game_roles, all_role_guesses, all_statements, [])
    #
    # stats = Statistics()
    # stats.add_result(game_result)
    # stats.print_results()
