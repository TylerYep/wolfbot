from const import logger
from encoder import WolfBotDecoder
import const
import json
from algorithms import switching_solver
from predictions import make_prediction, print_guesses, make_prediction_fast
from statistics import Statistics, GameResult

if __name__ == '__main__':
    with open('data/replay.json', 'r') as f:
       original_roles, game_roles, all_statements = json.load(f, cls=WolfBotDecoder)

    print('STATEMENTS: ')
    for i, s in enumerate(all_statements):
        print(s)
    logger.setLevel(0)
    logger.warning('[Hidden] Current roles: ' + str(original_roles[:const.NUM_PLAYERS]) +
            '\n\t Center cards:  ' + str(original_roles[const.NUM_PLAYERS:]) + '\n')
    logger.warning('[SOLUTION] Role guesses: ' + str(game_roles[:const.NUM_PLAYERS]) +
                '\n\t  Center cards: ' + str(game_roles[const.NUM_PLAYERS:]) + '\n')

    solution = switching_solver(all_statements)
    logger.warning(solution)

    all_role_guesses = make_prediction(solution)
    print_guesses(all_role_guesses)

    game_result = GameResult(game_roles, all_role_guesses, all_statements, [])

    stats = Statistics()
    stats.add_result(game_result)
    stats.print_statistics()
