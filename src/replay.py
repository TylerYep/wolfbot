""" replay.py """
import json
import random

from src import const
from src.one_night import simulate_game
from src.stats import Statistics


def replay_game_from_state() -> Statistics:
    """ Runs last game stored in replay_state.json. """
    with open(const.REPLAY_STATE) as f_replay:
        save_game = json.load(f_replay)
    game_state = save_game["rng_state"]
    rng_state = tuple([tuple(item) if isinstance(item, list) else item for item in game_state])
    random.setstate(rng_state)
    return simulate_game(enable_logging=True)
