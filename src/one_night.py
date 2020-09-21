""" one_night.py """
import heapq
import json
import logging
import random
from typing import Dict, List, Tuple

from tqdm import tqdm

from src import const, util
from src.const import Role, StatementLevel, Team, logger
from src.gui import GUIState
from src.roles import Player, get_role_obj
from src.statements import KnowledgeBase, Statement
from src.stats import GameResult, Statistics


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
    util.verify_const()
    if save_replay:
        with open(const.REPLAY_STATE, "w") as replay_file:
            json.dump({"rng_state": random.getstate()}, replay_file)

    game_roles = list(const.ROLES)
    if const.RANDOMIZE_ROLES:
        random.shuffle(game_roles)
    override_players(game_roles)
    original_roles = tuple(game_roles)

    gui_state = GUIState()
    gui_state.intro(original_roles)
    player_objs = night_falls(game_roles, original_roles)
    gui_state.night_falls()
    logger.info("\n-- GAME BEGINS --\n")
    all_statements = (
        get_player_multistatements(player_objs)
        if const.MULTI_STATEMENT
        else get_player_statements(player_objs)
    )
    gui_state.print_statements(all_statements)

    orig_wolf_inds = util.find_all_player_indices(original_roles, Role.WOLF)
    indiv_preds = get_individual_preds(player_objs, all_statements)
    most_freq_guesses, guessed_wolf_inds, vote_inds = get_voting_result(
        player_objs, indiv_preds
    )
    util.print_roles(game_roles, "Solution", logging.INFO)
    util.print_roles(most_freq_guesses, "WolfBot")
    _ = get_confidence(indiv_preds)
    winning_team = eval_winning_team(
        tuple(game_roles), list(guessed_wolf_inds), vote_inds
    )
    return GameResult(
        tuple(game_roles),
        most_freq_guesses,
        orig_wolf_inds,
        winning_team,
        all_statements,
    )


def get_player_multistatements(
    player_objs: Tuple[Player, ...]
) -> Tuple[Statement, ...]:
    """
    Returns array of each player's statements.
    TODO players should choose with what priority they want to speak
    """
    knowledge_base = KnowledgeBase()
    heap = [(i, i) for i in range(const.NUM_PLAYERS)]  # (priority, player_index) tuples
    heapq.heapify(heap)
    while heap:
        _, curr_ind = heapq.heappop(heap)
        if knowledge_base.final_claims[curr_ind].priority < StatementLevel.PRIMARY:
            player_objs[curr_ind].analyze(knowledge_base)
            statement = player_objs[curr_ind].get_statement(knowledge_base)
            player_objs[curr_ind].prev_priority = statement.priority
            knowledge_base.add(statement, curr_ind)
            logger.info(f"Player {curr_ind}: {statement.sentence}")

            if statement.priority < StatementLevel.PRIMARY:
                # New statements have priority at least NUM_PLAYERS
                # to ensure everyone spoke once
                new_priority = const.NUM_PLAYERS + random.randrange(len(heap) + 1)
                heapq.heappush(heap, (new_priority, curr_ind))

    return tuple(knowledge_base.final_claims)


def get_player_statements(player_objs: Tuple[Player, ...]) -> Tuple[Statement, ...]:
    """ Returns array of each player's statements. """
    knowledge_base = KnowledgeBase()
    curr_ind = 0
    while curr_ind < const.NUM_PLAYERS:
        player_objs[curr_ind].analyze(knowledge_base)
        statement = player_objs[curr_ind].get_statement(knowledge_base)
        knowledge_base.add(statement, curr_ind)
        logger.info(f"Player {curr_ind}: {statement.sentence}")
        curr_ind += 1
    return tuple(knowledge_base.final_claims)


def night_falls(
    game_roles: List[Role], original_roles: Tuple[Role, ...]
) -> Tuple[Player, ...]:
    """
    Initialize role object list and perform all switching and peeking actions.
    """
    if game_roles != list(original_roles):
        raise RuntimeError("game_roles should match original_roles.")
    logger.info("\n-- NIGHT FALLS --\n")
    util.print_roles(game_roles, "Hidden")

    # Awaken each player in order and initialize the Player object.
    player_objs = [Player(-1) for i in range(const.NUM_ROLES)]
    for awaken_role in const.AWAKE_ORDER:
        if awaken_role in const.ROLE_SET:
            logger.info(f"{awaken_role}, wake up.")
            role_obj = get_role_obj(awaken_role)
            for i in range(const.NUM_PLAYERS):
                if original_roles[i] is awaken_role:
                    player_objs[i] = role_obj.awake_init(i, game_roles, original_roles)
            logger.info(f"{awaken_role}, go to sleep.\n")

    # All other players wake up at the same time.
    logger.info("Everyone, wake up!\n")
    for i, role_name in enumerate(original_roles):
        if role_name in const.ROLE_SET - set(const.AWAKE_ORDER):
            role_obj = get_role_obj(role_name)
            player_objs[i] = role_obj.awake_init(i, game_roles, original_roles)

    return tuple(player_objs[: const.NUM_PLAYERS])


def get_individual_preds(
    player_objs: Tuple[Player, ...], all_statements: Tuple[Statement, ...]
) -> Tuple[Tuple[Role, ...], ...]:
    """ Let each player make a prediction of every player's true role. """
    logger.trace("\n[Trace] Predictions:")
    all_preds = [
        player_objs[i].predict(all_statements) for i in range(const.NUM_PLAYERS)
    ]
    number_length = len(str(const.NUM_ROLES))
    for i, pred in enumerate(all_preds):
        logger.trace(f"Player {i:{number_length}}: {pred}".replace("'", ""))
    return tuple(all_preds)


def get_confidence(
    all_role_guesses_arr: Tuple[Tuple[Role, ...], ...]
) -> Tuple[float, ...]:
    """
    Creates confidence levels for each prediction and takes most
    common role guess array as the final guess for that index.
    guess_histogram stores counts of prediction arrays.
    wolf_votes stores individual votes for Wolves.
    """
    confidence = []
    for i in range(const.NUM_ROLES):
        role_dict: Dict[Role, int] = {role: 0 for role in const.ROLE_SET}
        for prediction in all_role_guesses_arr:
            role_dict[prediction[i]] += 1
        count = max(role_dict.values())
        confidence.append(count / const.NUM_PLAYERS)

    logger.debug(f"Confidence levels: {[float(f'{conf:.2f}') for conf in confidence]}")
    return tuple(confidence)


def get_voting_result(
    player_objs: Tuple[Player, ...], all_role_guesses_arr: Tuple[Tuple[Role, ...], ...]
) -> Tuple[Tuple[Role, ...], Tuple[int, ...], Tuple[int, ...]]:
    """
    Creates confidence levels for each prediction and takes most
    common role guess array as the final guess for that index.
    guess_histogram stores counts of prediction arrays.
    wolf_votes stores individual votes for Wolves.
    """
    wolf_votes = [0] * const.NUM_PLAYERS
    vote_inds = []
    for i, prediction in enumerate(all_role_guesses_arr):
        vote_ind = player_objs[i].vote(prediction)
        wolf_votes[vote_ind] += 1
        vote_inds.append(vote_ind)

    logger.info(f"\nVote Array: {wolf_votes}\n")
    guess_histogram = const.get_counts(all_role_guesses_arr)
    avg_role_guesses, _ = max(guess_histogram.items(), key=lambda x: x[1])
    max_votes = max(wolf_votes)
    guessed_wolf_inds = [i for i, count in enumerate(wolf_votes) if count == max_votes]
    return avg_role_guesses, tuple(guessed_wolf_inds), tuple(vote_inds)


def eval_winning_team(
    game_roles: Tuple[Role, ...],
    guessed_wolf_inds: List[int],
    vote_inds: Tuple[int, ...],
) -> Team:
    """ Decide which team won based on the final vote. """
    killed_wolf, killed_tanner, villager_win = False, False, False
    if len(guessed_wolf_inds) == const.NUM_PLAYERS:
        logger.info("No wolves were found.")
        if final_wolf_inds := util.find_all_player_indices(game_roles, Role.WOLF):
            logger.info(f"But Player(s) {list(final_wolf_inds)} was a Wolf!\n")
        else:
            logger.info("That was correct!\n")
            villager_win = True
    else:
        # Hunter kills the player he voted for if he dies.
        for i in guessed_wolf_inds:
            logger.info(
                f"Player {i} was chosen as a Wolf.\nPlayer {i} was a {game_roles[i]}!\n"
            )
            if game_roles[i] is Role.HUNTER:
                if vote_inds[i] not in guessed_wolf_inds:
                    guessed_wolf_inds.append(vote_inds[i])
                logger.info(
                    f"(Player {i}) Hunter died and killed Player {vote_inds[i]} too!\n"
                )
            elif game_roles[i] is Role.WOLF:
                killed_wolf = True
            elif game_roles[i] is Role.TANNER:
                killed_tanner = True

    if villager_win or killed_wolf:
        logger.info("Village Team wins!")
        return Team.VILLAGE

    if killed_tanner:
        logger.info("Tanner wins!")
        return Team.TANNER

    logger.info("Werewolf Team wins!")
    return Team.WEREWOLF


def override_players(game_roles: List[Role]) -> None:
    """
    Makes changes to the randomized set of game_roles using the
    specifications in const.py. For example, we can swap a Wolf to
    the const.FIXED_WOLF_INDEX, or choose what player role we want to have.
    """
    if const.INTERACTIVE_MODE:
        if const.USER_ROLE is Role.NONE:
            user_index = random.randrange(const.NUM_PLAYERS)
            const.IS_USER[user_index] = True
        else:
            if role_inds := util.find_all_player_indices(game_roles, const.USER_ROLE):
                new_user_ind = random.choice(role_inds)
                const.IS_USER[new_user_ind] = True
            else:
                role_ind = game_roles.index(const.USER_ROLE)
                random_player_ind = random.randrange(const.NUM_PLAYERS)
                util.swap_characters(game_roles, role_ind, random_player_ind)

    if (
        const.FIXED_WOLF_INDEX is not None
        and (wolf_inds := util.find_all_player_indices(game_roles, Role.WOLF))
        and const.FIXED_WOLF_INDEX >= 0
    ):
        wolf_ind = random.choice(wolf_inds)
        if wolf_ind != const.FIXED_WOLF_INDEX:
            util.swap_characters(game_roles, wolf_ind, const.FIXED_WOLF_INDEX)
