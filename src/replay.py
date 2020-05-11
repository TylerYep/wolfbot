""" replay.py """
import json
import random

from src import const, util
from src.const import logger
from src.encoder import WolfBotDecoder
from src.one_night import simulate_game
from src.stats import GameResult, Statistics
from src.voting import consolidate_results


def replay_game_from_state() -> Statistics:
    """ Runs last game stored in replay_state.json. """
    with open(const.REPLAY_STATE) as f_replay:
        save_game = json.load(f_replay)
    game_state = save_game["rng_state"]
    rng_state = tuple([tuple(item) if isinstance(item, list) else item for item in game_state])
    random.setstate(rng_state)

    return simulate_game(disable_logging=False)


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

    util.print_roles(original_roles, "Hidden")
    util.print_roles(game_roles, "Solution")

    game_result = consolidate_results(save_game)
    stat_tracker = Statistics()
    stat_tracker.add_result(game_result)
    stat_tracker.print_statistics()

    return game_result
