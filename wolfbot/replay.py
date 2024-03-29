import json
import random

from wolfbot import const
from wolfbot.one_night import play_one_night_werewolf
from wolfbot.stats import GameResult, Statistics


def replay_game_from_state() -> GameResult:
    """Runs last game stored in replay_state.json."""
    with const.REPLAY_STATE.open(encoding="utf-8") as f_replay:
        save_game = json.load(f_replay)
    game_state = save_game["rng_state"]
    rng_state = tuple(
        tuple(item) if isinstance(item, list) else item for item in game_state
    )
    random.setstate(rng_state)

    game_result = play_one_night_werewolf(save_replay=False)
    stat_tracker = Statistics()
    stat_tracker.add_result(game_result)
    stat_tracker.print_statistics()
    return game_result
