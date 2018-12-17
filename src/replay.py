''' replay.py '''
import json

from statistics import Statistics, GameResult
from algorithms import switching_solver
from predictions import make_prediction, print_guesses
from encoder import WolfBotDecoder
from voting import consolidate_results
from const import logger
import const

def replay_game():
    ''' Runs last game stored in replay.json '''
    with open('data/replay.json', 'r') as f_replay:
        original_roles, game_roles, all_statements, player_objs = json.load(f_replay, cls=WolfBotDecoder)

    logger.setLevel(0)
    logger.warning('\n\nSTATEMENTS:\n')
    for sentence in all_statements:
        logger.warning(sentence)
    logger.warning('\n[Hidden] Current roles: %s\n\t Center cards: %s\n',
                   str(original_roles[:const.NUM_PLAYERS]), str(original_roles[const.NUM_PLAYERS:]))
    logger.warning('[SOLUTION] Role guesses: %s\n\t  Center cards: %s\n',
                   str(game_roles[:const.NUM_PLAYERS]), str(game_roles[const.NUM_PLAYERS:]))

    game_result = []
    if const.USE_VOTING:
        save_game = (original_roles, game_roles, all_statements, player_objs)
        game_result = consolidate_results(switching_solver, save_game)
    else:
        solution = switching_solver(all_statements)
        logger.warning('All Solver Solutions: ')
        for sol in solution:
            logger.warning(sol)
        all_role_guesses = make_prediction(solution)
        print_guesses(all_role_guesses)
        game_result = GameResult(game_roles, all_role_guesses, all_statements, [])

    stats = Statistics()
    stats.add_result(game_result)
    stats.print_statistics()

if __name__ == '__main__':
    replay_game()
