"""
train.py
To run: python -m src.learning.train
"""
import json
import os

# import time
from collections import defaultdict
from typing import Any, DefaultDict, List, Tuple

from src import const
from src.const import Role
from src.encoder import WolfBotDecoder, WolfBotEncoder
from src.one_night import simulate_game
from src.stats import GameResult


def evaluate(game: GameResult) -> int:
    """ Evaluation function. """
    val = 5
    for wolf_ind in game.wolf_inds:
        if game.guessed[wolf_ind] is Role.WOLF:
            val = -5
    return val


def get_wolf_state(
    game: GameResult,
) -> Tuple[List[Tuple[Tuple[int, ...], Tuple[str, ...]]], List[str]]:
    """ Fetches Wolf statement from Game. """
    states, statements = [], []
    for wolf_ind in game.wolf_inds:
        state = (game.wolf_inds, tuple([s.sentence for s in game.statements[:wolf_ind]]))
        states.append(state)
        statements.append(game.statements[wolf_ind].sentence)
    return states, statements


def remap_keys(
    mapping: DefaultDict[Any, DefaultDict[Any, float]]
) -> DefaultDict[Any, DefaultDict[Any, float]]:
    """ Remaps keys for jsonifying. """
    exp_dict: DefaultDict[Any, DefaultDict[Any, float]] = defaultdict(lambda: defaultdict(float))
    for k, val in mapping.items():
        exp_dict[str(k)] = val
    return exp_dict


def train(folder: str, eta: float = 0.01) -> None:
    """ Trains Wolf using games stored in simulations. """
    counter = 0
    experience_dict: DefaultDict[Any, DefaultDict[Any, float]] = defaultdict(
        lambda: defaultdict(float)
    )
    count_dict: DefaultDict[Any, int] = defaultdict(int)  # NOTE: For testing purposes
    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        if file_path.lower().endswith(".json"):
            with open(file_path) as data_file:
                for game in json.load(data_file, cls=WolfBotDecoder):
                    # See how training improves over time
                    if counter % 100 == 0:
                        test()
                    states, statements = get_wolf_state(game)
                    for state, statement in zip(states, statements):
                        experience_dict[state][statement] = (1 - eta) * experience_dict[state][
                            statement
                        ] + eta * evaluate(game)
                        count_dict[(state)] += 1
                    counter += 1

    exp_dict = remap_keys(experience_dict)
    with open("src/learning/simulations/wolf.json", "w") as wolf_file:
        # _{time.strftime('%Y%m%d_%H%M%S')}.json", "w") as wolf_file:
        json.dump(exp_dict, wolf_file, cls=WolfBotEncoder, indent=2)


def test() -> None:  # experience_dict as param
    """ Run play_one_night_werewolf with a specific experience_dict. """
    const.USE_RL_WOLF = False
    simulate_game(num_games=const.NUM_GAMES, enable_tqdm=True)


if __name__ == "__main__":
    train("src/learning/simulations")
