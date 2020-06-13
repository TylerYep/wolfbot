""" voting.py """
import logging
from typing import Dict, List, Tuple

from src import const, util
from src.algorithms import switching_solver as solver
from src.const import logger
from src.predictions import make_prediction
from src.roles import Player
from src.statements import Statement
from src.stats import GameResult, SavedGame


def consolidate_results(save_game: SavedGame) -> GameResult:
    """ Consolidates results and returns final GameResult. """
    original_roles, game_roles, all_statements, player_objs = save_game.load_game()
    orig_wolf_inds = util.find_all_player_indices(original_roles, "Wolf")

    if const.USE_VOTING:
        indiv_preds = get_individual_preds(player_objs, all_statements, orig_wolf_inds)
        all_guesses, guessed_wolf_inds, vote_inds = get_voting_result(player_objs, indiv_preds)
        util.print_roles(game_roles, "Solution", logging.INFO)
        util.print_roles(all_guesses, "WolfBot")
        _ = get_confidence(indiv_preds)
        winning_team = eval_winning_team(game_roles, guessed_wolf_inds, vote_inds)
        return GameResult(game_roles, all_guesses, orig_wolf_inds, winning_team)

    all_solutions = solver(tuple(all_statements))
    for solution in all_solutions:
        logger.trace(f"Solver interpretation: {solution.path}")
    all_role_guesses = list(make_prediction(all_solutions))
    util.print_roles(all_role_guesses, "WolfBot")
    return GameResult(game_roles, all_role_guesses, orig_wolf_inds)


def get_individual_preds(
    player_objs: List[Player], all_statements: List[Statement], orig_wolf_inds: List[int]
) -> List[Tuple[str, ...]]:
    """ Let each player make a prediction of every player's true role. """
    logger.trace("\n[Trace] Predictions:")
    all_predictions = [
        tuple(player_objs[i].get_prediction(all_statements, orig_wolf_inds))
        for i in range(const.NUM_PLAYERS)
    ]
    number_length = len(str(const.NUM_ROLES))
    for i, pred in enumerate(all_predictions):
        logger.trace(f"Player {i:{number_length}}: {pred}".replace("'", ""))

    return all_predictions


def get_confidence(all_role_guesses_arr: List[Tuple[str, ...]]) -> List[float]:
    """
    Creates confidence levels for each prediction and takes most
    common role guess array as the final guess for that index.
    guess_histogram stores counts of prediction arrays.
    wolf_votes stores individual votes for Wolves.
    """
    confidence = []
    for i in range(const.NUM_ROLES):
        role_dict: Dict[str, int] = {role: 0 for role in const.ROLE_SET}
        for prediction in all_role_guesses_arr:
            role_dict[prediction[i]] += 1
        count = max(role_dict.values())
        confidence.append(count / const.NUM_PLAYERS)

    logger.debug(f"Confidence levels: {[float(f'{conf:.2f}') for conf in confidence]}")
    return confidence


def get_voting_result(
    player_objs: List[Player], all_role_guesses_arr: List[Tuple[str, ...]]
) -> Tuple[List[str], List[int], List[int]]:
    """
    Creates confidence levels for each prediction and takes most
    common role guess array as the final guess for that index.
    guess_histogram stores counts of prediction arrays.
    wolf_votes stores individual votes for Wolves.
    """
    wolf_votes = [0] * const.NUM_PLAYERS
    vote_inds = []
    for i, prediction in enumerate(all_role_guesses_arr):
        vote_ind = player_objs[i].get_vote(prediction)
        wolf_votes[vote_ind] += 1
        vote_inds.append(vote_ind)

    logger.info(f"\nVote Array: {wolf_votes}\n")
    assert sum(wolf_votes) == const.NUM_PLAYERS

    guess_histogram = const.get_counts(all_role_guesses_arr)
    avg_role_guesses, _ = max(guess_histogram.items(), key=lambda x: x[1])
    max_votes = max(wolf_votes)
    guessed_wolf_inds = [i for i, count in enumerate(wolf_votes) if count == max_votes]

    return list(avg_role_guesses), guessed_wolf_inds, vote_inds


def eval_winning_team(
    game_roles: List[str], guessed_wolf_inds: List[int], vote_inds: List[int]
) -> str:
    """ Decide which team won based on the final vote. """
    killed_wolf, killed_tanner, villager_win = False, False, False
    if len(guessed_wolf_inds) == const.NUM_PLAYERS:
        logger.info("No wolves were found.")
        final_wolf_inds = util.find_all_player_indices(game_roles, "Wolf")
        if final_wolf_inds:
            logger.info(f"But Player(s) {final_wolf_inds} was a Wolf!\n")
        else:
            logger.info("That was correct!\n")
            villager_win = True
    else:
        # Hunter kills the player he voted for if he dies.
        for i in guessed_wolf_inds:
            logger.info(f"Player {i} was chosen as a Wolf.\nPlayer {i} was a {game_roles[i]}!\n")
            if game_roles[i] == "Hunter":
                if vote_inds[i] not in guessed_wolf_inds:
                    guessed_wolf_inds.append(vote_inds[i])
                logger.info(f"(Player {i}) Hunter died and killed Player {vote_inds[i]} too!\n")
            elif game_roles[i] == "Wolf":
                killed_wolf = True
            elif game_roles[i] == "Tanner":
                killed_tanner = True

    if villager_win or killed_wolf:
        logger.info("Village Team wins!")
        return "Villager"

    if killed_tanner:
        logger.info("Tanner wins!")
        return "Tanner"

    logger.info("Werewolf Team wins!")
    return "Werewolf"
