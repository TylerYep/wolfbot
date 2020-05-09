""" one_night.py """
import json
import random
from typing import Dict, List, Tuple, Union

from tqdm import tqdm

from src import const, util
from src.const import logger
from src.encoder import WolfBotEncoder
from src.roles import Player, get_role_obj
from src.statements import Statement
from src.stats import GameResult, SavedGame, Statistics
from src.voting import consolidate_results


def simulate_game(
    num_games: int = 1, save_replay: bool = False, disable_tqdm: bool = True
) -> Dict[str, float]:
    """ Collects statistics about several simulations of play_one_night_werewolf. """
    stat_tracker = Statistics()
    for _ in tqdm(range(num_games), disable=disable_tqdm):
        game_result = play_one_night_werewolf(save_replay)
        stat_tracker.add_result(game_result)
    stat_tracker.print_statistics()
    stat_results = stat_tracker.get_metric_results()
    return stat_results


def play_one_night_werewolf(save_replay: bool = True) -> GameResult:
    """ Plays one round of One Night Ultimate Werewolf. """
    game_roles = list(const.ROLES)
    if const.RANDOMIZE_ROLES:
        random.shuffle(game_roles)
    original_roles = tuple(game_roles)
    if const.FIXED_WOLF_INDEX is not None:
        override_wolf_index(game_roles)

    player_objs = night_falls(game_roles, original_roles)
    logger.info("\n-- GAME BEGINS --\n")
    all_statements = get_player_statements(player_objs)
    print_roles(game_roles, "Hidden")

    save_game = SavedGame(original_roles, game_roles, all_statements, player_objs)
    if save_replay:
        with open(const.REPLAY_FILE, "w") as replay_file:
            json.dump(save_game, replay_file, cls=WolfBotEncoder, indent=2)

    return consolidate_results(save_game)


def get_player_statements(player_objs: List[Player]) -> List[Statement]:
    """ Returns array of each player's statements. """
    if not const.MULTI_STATEMENT:
        stated_roles: List[str] = []
        given_statements: List[Statement] = []
        for j in range(const.NUM_PLAYERS):
            statement = player_objs[j].get_statement(stated_roles, given_statements)
            stated_roles.append(statement.speaker)
            given_statements.append(statement)
            logger.info(f"Player {j}: {statement.sentence}")
        return given_statements

    stated_roles = [""] * const.NUM_PLAYERS
    finished_speaking = [
        Statement("", priority=const.NOT_YET_SPOKEN) for _ in range(const.NUM_PLAYERS)
    ]
    curr_ind = 0
    while not all(val.priority == const.PRIMARY for val in finished_speaking):
        if finished_speaking[curr_ind].priority < const.PRIMARY:
            statement = player_objs[curr_ind].get_statement(stated_roles, finished_speaking)
            player_objs[curr_ind].prev_priority = statement.priority
            stated_roles[curr_ind] = statement.speaker
            finished_speaking[curr_ind] = statement
            logger.info(f"Player {curr_ind}: {statement.sentence}")
            # if const.ENTER_TO_ADVANCE: input()
        # TODO: allow random order
        curr_ind = (curr_ind + 1) % const.NUM_PLAYERS
    return finished_speaking


def night_falls(game_roles: List[str], original_roles: Tuple[str, ...]) -> List[Player]:
    """ Initialize role object list and perform all switching and peeking actions to begin. """
    logger.info("\n-- NIGHT FALLS --\n")
    print_roles(game_roles, "Hidden")

    # Awaken each player in order and initialize the Player object.
    player_objs = [Player(i) for i in range(const.NUM_ROLES)]
    for role_str in const.AWAKE_ORDER:
        logger.info(f"{role_str}, wake up.")
        role_obj = get_role_obj(role_str)
        for i in range(const.NUM_PLAYERS):
            if original_roles[i] == role_str:
                player_objs[i] = role_obj.awake_init(i, game_roles, original_roles)
        logger.info(f"{role_str}, go to sleep.\n")

    # All other players wake up at the same time.
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


def print_roles(game_roles: Union[List[Player], List[str]], tag: str) -> None:
    """ Formats hidden roles to console. """
    role_output = (
        f'[{tag}] Current roles: {game_roles[:const.NUM_PLAYERS]}\n{" " * 10}'
        f"Center cards: {game_roles[const.NUM_PLAYERS:]}\n"
    )
    logger.debug(role_output.replace("'", ""))
