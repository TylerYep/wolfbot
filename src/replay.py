''' replay.py '''
import json

from statistics import Statistics, GameResult
from algorithms import switching_solver
from predictions import make_prediction, print_guesses
from encoder import WolfBotDecoder
from const import logger
import const

def replay_game():
    ''' Runs last game stored in replay.json '''
    with open('data/replay.json', 'r') as f_replay:
        original_roles, game_roles, all_statements = json.load(f_replay, cls=WolfBotDecoder)

    logger.warning('STATEMENTS: ')
    for _, sentence in enumerate(all_statements):
        logger.warning(sentence)
    logger.setLevel(0)
    logger.warning('[Hidden] Current roles: %s\n\t Center cards: %s\n',
                   str(original_roles[:const.NUM_PLAYERS]), str(original_roles[const.NUM_PLAYERS:]))
    logger.warning('[SOLUTION] Role guesses: %s\n\t  Center cards: %s\n',
                   str(game_roles[:const.NUM_PLAYERS]), str(game_roles[const.NUM_PLAYERS:]))

    solution = switching_solver(all_statements)
    logger.warning(solution)

    all_role_guesses = make_prediction(solution)
    print_guesses(all_role_guesses)

    game_result = GameResult(game_roles, all_role_guesses, all_statements, [])
    stats = Statistics()
    stats.add_result(game_result)
    stats.print_statistics()

if __name__ == '__main__':
    replay_game()
