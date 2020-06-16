""" one_night.py """
import json
import logging
import random
from typing import List, Tuple

from tqdm import tqdm

from src import const, util
from src.const import StatementLevel, logger
from src.encoder import WolfBotEncoder
from src.gui import GUIState
from src.roles import Player, get_role_obj
from src.statements import Statement
from src.stats import GameResult, SavedGame, Statistics
from src.voting import consolidate_results


def simulate_game(
    num_games: int = 1,
    save_replay: bool = False,
    enable_tqdm: bool = False,
    enable_logging: bool = False,
) -> Statistics:
    """ Collects statistics about several simulations of play_one_night_werewolf. """
    if not enable_logging:
        logger.set_level(logging.WARNING)

    stat_tracker = Statistics()
    for _ in tqdm(range(num_games), disable=not enable_tqdm):
        game_result = play_one_night_werewolf(save_replay)
        stat_tracker.add_result(game_result)
    stat_tracker.print_statistics()
    return stat_tracker


def play_one_night_werewolf(save_replay: bool = True) -> GameResult:
    """ Plays one round of One Night Ultimate Werewolf. """
    random_state = {"rng_state": random.getstate()}
    game_roles = list(const.ROLES)
    if const.RANDOMIZE_ROLES:
        random.shuffle(game_roles)
    original_roles = tuple(game_roles)
    if const.FIXED_WOLF_INDEX is not None:
        override_wolf_index(game_roles)

    gui_state = GUIState()
    gui_state.intro(original_roles)
    player_objs = night_falls(game_roles, original_roles)
    gui_state.night_falls()
    logger.info("\n-- GAME BEGINS --\n")
    all_statements = get_player_statements(player_objs)
    gui_state.print_statements(all_statements)

    save_game = SavedGame(original_roles, game_roles, all_statements, player_objs)
    if save_replay:
        with open(const.REPLAY_STATE, "w") as replay_file:
            json.dump(random_state, replay_file)
        with open(const.REPLAY_FILE, "w") as replay_file:
            json.dump(save_game, replay_file, cls=WolfBotEncoder, indent=2)

    return consolidate_results(save_game)


def get_player_statements(player_objs: List[Player]) -> List[Statement]:
    """ Returns array of each player's statements. """
    stated_roles: List[str] = []
    given_statements: List[Statement] = []

    if not const.MULTI_STATEMENT:
        for j in range(const.NUM_PLAYERS):
            statement = player_objs[j].get_statement(stated_roles, given_statements)
            stated_roles.append(statement.speaker)
            given_statements.append(statement)
            logger.info(f"Player {j}: {statement.sentence}")
        return given_statements

    finished_speaking = [
        Statement("", priority=StatementLevel.NOT_YET_SPOKEN) for _ in range(const.NUM_PLAYERS)
    ]
    curr_ind = 0
    while not all(val.priority == StatementLevel.PRIMARY for val in finished_speaking):
        if finished_speaking[curr_ind].priority < StatementLevel.PRIMARY:
            statement = player_objs[curr_ind].get_statement(stated_roles, finished_speaking)
            given_statements.append(statement)
            if len(stated_roles) <= curr_ind:
                stated_roles.append(statement.speaker)
            else:
                stated_roles[curr_ind] = statement.speaker
            finished_speaking[curr_ind] = statement
            logger.info(f"Player {curr_ind}: {statement.sentence}")
        # TODO: allow random order
        curr_ind = (curr_ind + 1) % const.NUM_PLAYERS
    return finished_speaking


def night_falls(game_roles: List[str], original_roles: Tuple[str, ...]) -> List[Player]:
    """ Initialize role object list and perform all switching and peeking actions to begin. """
    assert game_roles == list(original_roles)
    logger.info("\n-- NIGHT FALLS --\n")
    util.print_roles(game_roles, "Hidden")

    # Awaken each player in order and initialize the Player object.
    player_objs = [Player(i) for i in range(const.NUM_ROLES)]
    for role_str in const.AWAKE_ORDER:
        if role_str in const.ROLE_SET:
            logger.info(f"{role_str}, wake up.")
            role_obj = get_role_obj(role_str)
            for i in range(const.NUM_PLAYERS):
                if original_roles[i] == role_str:
                    player_objs[i] = role_obj.awake_init(i, game_roles, original_roles)
            logger.info(f"{role_str}, go to sleep.\n")

    # All other players wake up at the same time.
    logger.info("Everyone, wake up!\n")
    for i, role_str in enumerate(original_roles):
        if role_str in const.ROLE_SET - set(const.AWAKE_ORDER):
            role_obj = get_role_obj(role_str)
            player_objs[i] = role_obj.awake_init(i, game_roles, original_roles)

    return player_objs[: const.NUM_PLAYERS]


def override_wolf_index(game_roles: List[str]) -> None:
    """ Swap a Wolf to the const.FIXED_WOLF_INDEX. """
    wolf_inds = util.find_all_player_indices(game_roles, "Wolf")
    if wolf_inds and const.FIXED_WOLF_INDEX >= 0:
        wolf_ind = random.choice(wolf_inds)
        util.swap_characters(game_roles, wolf_ind, const.FIXED_WOLF_INDEX)
