''' voting.py '''
from typing import Dict, List, Tuple
import random
from collections import defaultdict

from src.stats import GameResult, SavedGame
from src.algorithms import switching_solver
from src.predictions import make_prediction, print_guesses
from src.statements import Statement
from src.roles import Player
from src.const import logger
from src import const, util

def consolidate_results(save_game: SavedGame) -> GameResult:
    ''' Consolidates results and returns final GameResult. '''
    original_roles, game_roles, all_statements, player_objs = save_game.load_game()
    orig_wolf_inds = util.find_all_player_indices(original_roles, 'Wolf')
    if const.USE_VOTING:
        indiv_preds = get_individual_preds(player_objs, all_statements, orig_wolf_inds)
        all_guesses, confidence, guessed_wolf_inds, vote_inds = get_voting_result(indiv_preds)
        print_guesses(all_guesses)
        logger.debug(f'Confidence level: {[float(f"{conf:.2f}") for conf in confidence]}')
        winning_team = eval_final_guesses(game_roles, guessed_wolf_inds, vote_inds)
        return GameResult(game_roles, all_guesses, orig_wolf_inds, winning_team)

    all_solutions = switching_solver(tuple(all_statements))
    for solution in all_solutions:
        logger.log(const.TRACE, f'Solver interpretation: {solution.path}')
    all_role_guesses = make_prediction(all_solutions)
    print_guesses(all_role_guesses)
    return GameResult(game_roles, all_role_guesses, orig_wolf_inds)


def is_player_evil(player_objs: List[Player], i: int, orig_wolf_inds: List[int]) -> bool:
    ''' Decide whether a character is about to make an evil prediction. '''
    # TODO When a wolf becomes good? Do I need to check for Wolf twice?
    return (i in orig_wolf_inds and player_objs[i].new_role == '') \
        or (player_objs[i].role in const.EVIL_ROLES and player_objs[i].new_role == '') \
        or player_objs[i].new_role in const.EVIL_ROLES


def get_individual_preds(player_objs: List[Player],
                         all_statements: List[Statement],
                         orig_wolf_inds: List[int]) -> List[List[str]]:
    ''' Let each player make a prediction of every player's true role. '''
    all_role_guesses_arr = []
    # Good player vs Bad player guesses
    for i in range(const.NUM_PLAYERS):
        all_solutions = switching_solver(tuple(all_statements), i)
        is_evil = is_player_evil(player_objs, i, orig_wolf_inds)
        prediction = make_prediction(all_solutions, is_evil)
        all_role_guesses_arr.append(prediction)

    for pred in all_role_guesses_arr:
        logger.log(const.TRACE, f'Player prediction: {pred}'.replace('\'', ''))
    return all_role_guesses_arr


def eval_final_guesses(game_roles: List[str],
                       guessed_wolf_inds: List[int],
                       vote_inds: List[int]) -> str:
    ''' Decide which team won based on the final vote. '''
    killed_wolf, killed_tanner, villager_win = False, False, False
    if len(guessed_wolf_inds) == const.NUM_PLAYERS:
        logger.info('No wolves were found.')
        final_wolf_inds = util.find_all_player_indices(game_roles, 'Wolf')
        if final_wolf_inds:
            logger.info(f'But Player(s) {final_wolf_inds} was a Wolf!\n')
        else:
            logger.info('That was correct!\n')
            villager_win = True
    else:
        # Hunter kills the player he voted for if he dies.
        # Ensure player did not vote themselves in this case.
        for i in guessed_wolf_inds:
            if game_roles[i] == 'Hunter' and i != vote_inds[i]:
                guessed_wolf_inds.append(vote_inds[i])
                logger.info(f'(Player {i}) Hunter died and killed Player {vote_inds[i]} too!\n')
            elif game_roles[i] == 'Wolf':
                killed_wolf = True
            elif game_roles[i] == 'Tanner':
                killed_tanner = True

            logger.info(f'Player {i} was chosen as a Wolf.\n' +
                        f'Player {i} was a {game_roles[i]}!\n')

    if villager_win or killed_wolf:
        logger.info('Village Team wins!')
        return 'Villager'

    if killed_tanner:
        logger.info('Tanner wins!')
        return 'Tanner'

    logger.info('Werewolf Team wins!')
    return 'Werewolf'


def get_voting_result(all_role_guesses_arr: List[List[str]]) \
                      -> Tuple[List[str], List[float], List[int], List[int]]:
    '''
    Creates confidence levels for each prediction and takes most
    common role guess array as the final guess for that index.
    guess_histogram stores counts of prediction arrays.
    wolf_votes stores individual votes for Wolves.
    '''
    guess_histogram: Dict[Tuple[str, ...], int] = defaultdict(int)
    wolf_votes = [0 for _ in range(const.NUM_PLAYERS)]
    vote_inds = []
    for i, prediction in enumerate(all_role_guesses_arr):
        guess_histogram[tuple(prediction)] += 1
        vote_ind = get_player_vote(i, prediction)
        wolf_votes[vote_ind] += 1
        vote_inds.append(vote_ind)

    logger.debug(f'Vote Array: {wolf_votes}')
    assert sum(wolf_votes) == const.NUM_PLAYERS

    all_role_guesses, _ = max(guess_histogram.items(), key=lambda x: x[1])
    guessed_wolf_inds = [i for i, count in enumerate(wolf_votes) if count == max(wolf_votes)]

    confidence = []
    for i in range(const.NUM_ROLES):
        role_dict: Dict[str, int] = defaultdict(int)
        for prediction in all_role_guesses_arr:
            role_dict[prediction[i]] += 1
        count = max(role_dict.values())
        confidence.append(count / const.NUM_PLAYERS)

    return list(all_role_guesses), confidence, guessed_wolf_inds, vote_inds


def get_player_vote(ind: int, prediction: List[str]) -> int:
    ''' Updates Wolf votes for a given prediction. '''
    # TODO find the most likely Wolf and only vote for that one
    wolf_inds = util.find_all_player_indices(prediction, 'Wolf')
    if wolf_inds:
        return random.choice(wolf_inds)
    # There are some really complicated game mechanics for the Minion.
    # https://boardgamegeek.com/thread/1422062/pointing-center-free-parking
    return (ind + 1) % const.NUM_PLAYERS
