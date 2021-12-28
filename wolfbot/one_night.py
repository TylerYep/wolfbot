import heapq
import json
import logging
import random

from tqdm import trange  # type: ignore[import]

from wolfbot import const
from wolfbot.enums import Role, StatementLevel, Team
from wolfbot.game_utils import (
    find_all_player_indices,
    get_player,
    print_roles,
    swap_characters,
)
from wolfbot.log import logger
from wolfbot.roles import Player, get_role_obj
from wolfbot.statements import KnowledgeBase, Statement
from wolfbot.stats import GameResult, Statistics
from wolfbot.user import UserState
from wolfbot.util import get_counts


def simulate_game(
    num_games: int = 1,
    save_replay: bool = False,
    enable_tqdm: bool = False,
    enable_logging: bool = False,
) -> Statistics:
    """Collects statistics about several simulations of play_one_night_werewolf."""
    if not enable_logging:
        logger.set_level(logging.WARNING)
    stat_tracker = Statistics()
    for _ in trange(num_games, disable=not enable_tqdm):
        game_result = play_one_night_werewolf(save_replay)
        stat_tracker.add_result(game_result)
    stat_tracker.print_statistics()
    return stat_tracker


def play_one_night_werewolf(save_replay: bool = True) -> GameResult:
    """Plays one round of One Night Ultimate Werewolf."""
    setup_game(save_replay)
    original_roles, orig_wolf_inds = init_game_roles()
    player_objs, game_roles = night_falls(original_roles)
    all_statements = (
        get_player_multistatements(player_objs)
        if const.MULTI_STATEMENT
        else get_player_statements(player_objs)
    )
    UserState.print_statements(all_statements)
    all_predictions = get_individual_preds(player_objs, all_statements)
    most_freq_guesses, guessed_wolf_inds, player_votes = get_voting_result(
        player_objs, all_predictions
    )
    print_analysis(game_roles, most_freq_guesses, all_predictions)
    winning_team = eval_winning_team(game_roles, list(guessed_wolf_inds), player_votes)
    return GameResult(
        game_roles, most_freq_guesses, orig_wolf_inds, winning_team, all_statements
    )


def setup_game(save_replay: bool) -> None:
    """Miscellaneous setup steps."""
    const.verify_valid_const_config(const)
    if save_replay:
        with open(const.REPLAY_STATE, "w", encoding="utf-8") as replay_file:
            json.dump({"rng_state": random.getstate()}, replay_file)


def init_game_roles() -> tuple[tuple[Role, ...], tuple[int, ...]]:
    """Returns the randomized game_roles and wolf_inds."""
    game_roles = list(const.ROLES)
    if const.RANDOMIZE_ROLES:
        random.shuffle(game_roles)
    override_players(game_roles)
    UserState.intro(game_roles)
    return tuple(game_roles), find_all_player_indices(game_roles, Role.WOLF)


def night_falls(
    original_roles: tuple[Role, ...]
) -> tuple[tuple[Player, ...], tuple[Role, ...]]:
    """
    Initialize role object list and perform all switching and peeking actions.

    Roles that find other roles go first in AWAKE_ORDER (e.g. Masons), which
    means we don't need to pass in original_roles to these constructors.
    The Doppelganger can take actions after these role types complete.
    """
    logger.info("\n-- NIGHT FALLS --\n")
    print_roles(original_roles, "Hidden")

    # Awaken each player in order and initialize the Player object.
    game_roles = list(original_roles)
    player_objs = [Player(-1) for _ in range(const.NUM_ROLES)]
    for awaken_role in const.AWAKE_ORDER:
        if awaken_role in const.ROLE_SET:
            logger.info(f"{awaken_role}, wake up.")
            role_obj = get_role_obj(awaken_role)
            for i in range(const.NUM_PLAYERS):
                if original_roles[i] is awaken_role:
                    player_objs[i] = role_obj.awake_init(i, game_roles)
            logger.info(f"{awaken_role}, go to sleep.\n")

    # All other players wake up at the same time.
    logger.info("Everyone, wake up!\n")
    for i, role_name in enumerate(original_roles):
        if role_name in const.ROLE_SET - set(const.AWAKE_ORDER):
            role_obj = get_role_obj(role_name)
            player_objs[i] = role_obj.awake_init(i, game_roles)

    UserState.night_falls()
    logger.info("\n-- GAME BEGINS --\n")
    return tuple(player_objs[: const.NUM_PLAYERS]), tuple(game_roles)


def get_player_multistatements(
    player_objs: tuple[Player, ...]
) -> tuple[Statement, ...]:
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


def get_player_statements(player_objs: tuple[Player, ...]) -> tuple[Statement, ...]:
    """Returns array of each player's statements."""
    knowledge_base = KnowledgeBase()
    curr_ind = 0
    while curr_ind < const.NUM_PLAYERS:
        player_objs[curr_ind].analyze(knowledge_base)
        statement = player_objs[curr_ind].get_statement(knowledge_base)
        knowledge_base.add(statement, curr_ind)
        logger.info(f"Player {curr_ind}: {statement.sentence}")
        curr_ind += 1
    return tuple(knowledge_base.final_claims)


def get_individual_preds(
    player_objs: tuple[Player, ...], all_statements: tuple[Statement, ...]
) -> tuple[tuple[Role, ...], ...]:
    """Let each player make a prediction of every player's true role."""
    logger.trace("\n[Trace] Predictions:")
    all_preds = [
        player_objs[i].predict(all_statements) for i in range(const.NUM_PLAYERS)
    ]
    number_length = len(str(const.NUM_ROLES))
    for i, pred in enumerate(all_preds):
        logger.trace(f"Player {i:{number_length}}: {pred}".replace("'", ""))
    return tuple(all_preds)


def get_confidence(all_predictions: tuple[tuple[Role, ...], ...]) -> tuple[float, ...]:
    """
    Creates confidence levels for each prediction and takes most
    common role guess array as the final guess for that index.
    guess_histogram stores counts of prediction arrays.
    wolf_votes stores individual votes for Wolves.
    """
    confidence = []
    for i in range(const.NUM_ROLES):
        role_dict: dict[Role, int] = {role: 0 for role in const.ROLE_SET}
        for prediction in all_predictions:
            role_dict[prediction[i]] += 1
        count = max(role_dict.values())
        confidence.append(count / const.NUM_PLAYERS)

    logger.debug(f"Confidence levels: {[float(f'{conf:.2f}') for conf in confidence]}")
    return tuple(confidence)


def print_analysis(
    game_roles: tuple[Role, ...],
    most_freq_guesses: tuple[Role, ...],
    indiv_preds: tuple[tuple[Role, ...], ...],
) -> None:
    print_roles(game_roles, "Solution", logging.INFO)
    print_roles(most_freq_guesses, "WolfBot")
    _ = get_confidence(indiv_preds)


def get_voting_result(
    player_objs: tuple[Player, ...], all_predictions: tuple[tuple[Role, ...], ...]
) -> tuple[tuple[Role, ...], tuple[int, ...], tuple[int, ...]]:
    """
    Creates confidence levels for each prediction and takes most common role guess
    array as the final guess for that index.

    - guess_histogram stores counts of prediction arrays.
    - wolf_votes stores individual votes for Wolves.
    """
    wolf_votes = [0] * const.NUM_PLAYERS
    if const.INTERACTIVE_MODE and const.INFLUENCE_PROB == 1:
        # Convince other players to vote with you.
        logger.info(
            "\nAll players trust you. Who should everyone vote for? "
            "(If you think there are no Wolves, vote for yourself.)"
        )
        vote_ind = get_player(is_user=True)
        if vote_ind == const.IS_USER.index(True):
            wolf_votes = [1] * const.NUM_PLAYERS
            player_votes = [
                (i + 1) % const.NUM_PLAYERS for i in range(const.NUM_PLAYERS)
            ]
        else:
            wolf_votes[vote_ind] += const.NUM_PLAYERS
            player_votes = [vote_ind] * const.NUM_PLAYERS
    else:
        player_votes = []
        for i, prediction in enumerate(all_predictions):
            vote_ind = player_objs[i].vote(prediction)
            wolf_votes[vote_ind] += 1
            player_votes.append(vote_ind)

    assert len(player_votes) == const.NUM_PLAYERS
    logger.info(f"\nVote Array: {wolf_votes}\n")
    guess_histogram = get_counts(all_predictions)
    avg_role_guesses, _ = max(guess_histogram.items(), key=lambda x: x[1])
    max_votes = max(wolf_votes)
    guessed_wolf_inds = [i for i, count in enumerate(wolf_votes) if count == max_votes]
    return avg_role_guesses, tuple(guessed_wolf_inds), tuple(player_votes)


def eval_winning_team(
    game_roles: tuple[Role, ...],
    guessed_wolf_inds: list[int],
    player_votes: tuple[int, ...],
) -> Team:
    """Decide which team won based on the final vote."""
    killed_wolf, killed_tanner, villager_win = False, False, False
    if len(guessed_wolf_inds) == const.NUM_PLAYERS:
        logger.info("No wolves were found.")
        if final_wolf_inds := find_all_player_indices(game_roles, Role.WOLF):
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
                if player_votes[i] not in guessed_wolf_inds:
                    guessed_wolf_inds.append(player_votes[i])
                logger.info(
                    f"(Player {i}) Hunter died and killed "
                    f"Player {player_votes[i]} too!\n"
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


def override_players(game_roles: list[Role]) -> None:
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
            if role_inds := find_all_player_indices(game_roles, const.USER_ROLE):
                new_user_ind = random.choice(role_inds)
                const.IS_USER[new_user_ind] = True
            else:
                role_ind = game_roles.index(const.USER_ROLE)
                random_player_ind = random.randrange(const.NUM_PLAYERS)
                swap_characters(game_roles, role_ind, random_player_ind)

    if (
        const.FIXED_WOLF_INDEX is not None
        and (wolf_inds := find_all_player_indices(game_roles, Role.WOLF))
        and const.FIXED_WOLF_INDEX >= 0
    ):
        wolf_ind = random.choice(wolf_inds)
        if wolf_ind != const.FIXED_WOLF_INDEX:
            swap_characters(game_roles, wolf_ind, const.FIXED_WOLF_INDEX)
