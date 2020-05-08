""" replay.py """
import json

from src import const
from src.const import logger
from src.encoder import WolfBotDecoder
from src.one_night import print_roles
from src.stats import GameResult, Statistics
from src.voting import consolidate_results


def replay_game() -> GameResult:
    """ Runs last game stored in replay.json. """
    with open(const.REPLAY_FILE) as f_replay:
        save_game = json.load(f_replay, cls=WolfBotDecoder)
    original_roles, game_roles, all_statements, player_objs = save_game.load_game()

    logger.setLevel(0)
    logger.warning(player_objs)
    logger.warning("\n\nSTATEMENTS:\n")
    for sentence in all_statements:
        logger.warning(sentence)

    print_roles(original_roles, "Hidden")
    print_roles(game_roles, "Solution")
    # logger.warning((f'[SOLUTION] Role guesses: {game_roles[:const.NUM_PLAYERS]}\n' + ' '*11 +
    #                 f'Center cards: {game_roles[const.NUM_PLAYERS:]}\n').replace('\'', ''))

    game_result = consolidate_results(save_game)
    stat_tracker = Statistics()
    stat_tracker.add_result(game_result)
    stat_tracker.print_statistics()

    return game_result
