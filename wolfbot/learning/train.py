"""
train.py
To run: python -m wolfbot.learning.train
"""
import json

# import time
from collections import defaultdict
from pathlib import Path
from typing import Any

from wolfbot import const
from wolfbot.const import Role
from wolfbot.encoder import WolfBotDecoder, WolfBotEncoder
from wolfbot.one_night import simulate_game
from wolfbot.stats import GameResult


def evaluate(game: GameResult) -> int:
    """Evaluation function."""
    val = 5
    for wolf_ind in game.wolf_inds:
        if game.guessed[wolf_ind] is Role.WOLF:
            val = -5
    return val


def get_wolf_state(
    game: GameResult,
) -> tuple[list[tuple[tuple[int, ...], tuple[str, ...]]], list[str]]:
    """Fetches Wolf statement from Game."""
    states, statements = [], []
    for wolf_ind in game.wolf_inds:
        state = (game.wolf_inds, tuple(s.sentence for s in game.statements[:wolf_ind]))
        states.append(state)
        statements.append(game.statements[wolf_ind].sentence)
    return states, statements


def remap_keys(
    mapping: defaultdict[Any, defaultdict[Any, float]]
) -> defaultdict[Any, defaultdict[Any, float]]:
    """Remaps keys for jsonifying."""
    exp_dict: defaultdict[Any, defaultdict[Any, float]] = defaultdict(
        lambda: defaultdict(float)
    )
    for k, val in mapping.items():
        exp_dict[str(k)] = val
    return exp_dict


def train(folder: str, eta: float = 0.01) -> None:
    """Trains Wolf using games stored in simulations."""
    counter = 0
    experience_dict: defaultdict[Any, defaultdict[Any, float]] = defaultdict(
        lambda: defaultdict(float)
    )
    count_dict: defaultdict[Any, int] = defaultdict(int)  # NOTE: For testing purposes
    for filepath in Path(folder).glob("*.json"):
        with open(filepath, encoding="utf-8") as data_file:
            for game in json.load(data_file, cls=WolfBotDecoder):
                # See how training improves over time
                if counter % 100 == 0:
                    test()
                states, statements = get_wolf_state(game)
                for state, statement in zip(states, statements):
                    experience_dict[state][statement] = (1 - eta) * experience_dict[
                        state
                    ][statement] + eta * evaluate(game)
                    count_dict[(state)] += 1
                counter += 1

    exp_dict = remap_keys(experience_dict)
    with open(
        "wolfbot/learning/simulations/wolf.json", "w", encoding="utf-8"
    ) as wolf_file:
        # _{time.strftime('%Y%m%d_%H%M%S')}.json", "w") as wolf_file:
        json.dump(exp_dict, wolf_file, cls=WolfBotEncoder, indent=2)


def test() -> None:  # experience_dict as param
    """Run play_one_night_werewolf with a specific experience_dict."""
    const.RL_WOLF = False
    simulate_game(num_games=const.NUM_GAMES, enable_tqdm=True)


if __name__ == "__main__":
    train("wolfbot/learning/simulations")
