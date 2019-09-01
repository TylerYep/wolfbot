''' replay.py '''
import json

from src.stats import Statistics, GameResult
from src.algorithms import switching_solver
from src.predictions import make_prediction, print_guesses
from src.encoder import WolfBotDecoder
from src.voting import consolidate_results
from src.const import logger
from src import const

def replay_game() -> None:
    ''' Runs last game stored in replay.json '''
    with open('data/replay.json', 'r') as f_replay:
        original_roles, game_roles, all_statements, player_objs \
                     = json.load(f_replay, cls=WolfBotDecoder)

    logger.setLevel(0)
    logger.warning('\n\nSTATEMENTS:\n')
    for sentence in all_statements:
        logger.warning(sentence)

    logger.warning(f'\n[Hidden] Current roles: {original_roles[:const.NUM_PLAYERS]} \
                    \n\t Center cards: {original_roles[const.NUM_PLAYERS:]}\n')
    logger.warning(f'[SOLUTION] Role guesses: {game_roles[:const.NUM_PLAYERS]} \
                    \n\t  Center cards: {game_roles[const.NUM_PLAYERS:]}\n')

    game_result = []
    if const.USE_VOTING:
        save_game = (original_roles, game_roles, all_statements, player_objs)
        game_result = consolidate_results(save_game)
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
