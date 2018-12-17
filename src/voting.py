''' voting.py '''
from statistics import GameResult
from collections import defaultdict
from util import find_all_player_indices
from algorithms import switching_solver
from predictions import make_prediction, print_guesses
from const import logger
import const

def consolidate_results(save_game):
    ''' Consolidates results and returns final GameResult. '''
    ORIGINAL_ROLES, game_roles, all_statements, player_objs = save_game
    if const.USE_VOTING:
        orig_wolf_inds = find_all_player_indices(ORIGINAL_ROLES, 'Wolf')
        all_role_guesses_arr = []
        for i in range(const.NUM_PLAYERS):
            # Good player vs Bad player guesses
            all_solutions = switching_solver(all_statements, i)     # TODO when a wolf becomes good?
            is_evil = (i in orig_wolf_inds and player_objs[i].new_role == '') \
                        or player_objs[i].new_role == 'Wolf'
            all_role_guesses_arr.append(make_prediction(all_solutions, is_evil))

        for prediction in all_role_guesses_arr:
            logger.log(const.logging.TRACE, 'Player prediction: %s', str(prediction))
        all_role_guesses, confidence, guessed_wolf_inds = get_voting_result(all_role_guesses_arr)
        print_guesses(all_role_guesses)
        logger.debug('Confidence level: %s', str([float('{0:0.2f}'.format(n)) for n in confidence]))
        winning_team = eval_wolf_guesses(game_roles, guessed_wolf_inds)
        return GameResult(game_roles, all_role_guesses, all_statements, orig_wolf_inds, winning_team)

    all_solutions = switching_solver(all_statements)
    for solution in all_solutions:
        logger.log(const.logging.TRACE, 'Solver interpretation: %s', str(solution.path))
    all_role_guesses = make_prediction(all_solutions)
    print_guesses(all_role_guesses)
    return GameResult(game_roles, all_role_guesses, all_statements, orig_wolf_inds)


def eval_wolf_guesses(game_roles, guessed_wolf_inds):
    ''' Decide which team won based on the final vote. '''
    killed_wolf = False
    killed_tanner = False
    villager_win = False
    if len(guessed_wolf_inds) == const.NUM_PLAYERS:
        logger.info('No wolves were found.')
        final_wolf_inds = find_all_player_indices(game_roles[:const.NUM_PLAYERS], 'Wolf')
        if final_wolf_inds:
            logger.info('But Player(s) %s was a Wolf!\n', str(final_wolf_inds))
        else:
            logger.info('That was correct!\n')
            villager_win = True
    else:
        for chosen_wolf in guessed_wolf_inds:
            if game_roles[chosen_wolf] == 'Wolf':
                killed_wolf = True
            elif game_roles[chosen_wolf] == 'Tanner':
                killed_tanner = True

            logger.info('Player %d was chosen as a Wolf.\nPlayer %d was a %s!\n',
                        chosen_wolf, chosen_wolf, game_roles[chosen_wolf])

    if villager_win or killed_wolf:
        logger.info('Village Team wins!')
        return 'Villager'

    if killed_tanner:
        logger.info('Tanner wins!')
        return 'Tanner'

    logger.info('Werewolf Team wins!')
    return 'Werewolf'


def get_voting_result(all_role_guesses_arr):
    '''
    Creates confidence levels for each prediction and takes most
    common role guess array as the final guess for that index.
    guess_histogram stores counts of prediction arrays.
    wolf_votes stores individual votes for Wolves.
    '''
    guess_histogram = defaultdict(int)
    wolf_votes = [0 for _ in range(const.NUM_PLAYERS)]
    for i, prediction in enumerate(all_role_guesses_arr):
        guess_histogram[tuple(prediction)] += 1
        wolf_votes[get_player_vote(i, prediction)] += 1

    logger.debug('Vote Array: %s', str(wolf_votes))
    assert sum(wolf_votes) == const.NUM_PLAYERS

    guessed_wolf_inds = [i for i, count in enumerate(wolf_votes) if count == max(wolf_votes)]
    all_role_guesses, _ = max(guess_histogram.items(), key=lambda x: x[1])
    confidence = []
    for i in range(const.NUM_ROLES):
        role_dict = defaultdict(int)
        for prediction in all_role_guesses_arr:
            role_dict[prediction[i]] += 1
        count = max(role_dict.values())
        confidence.append(count / const.NUM_PLAYERS)

    return list(all_role_guesses), confidence, guessed_wolf_inds


def get_player_vote(ind, prediction):
    ''' Updates Wolf votes for a given prediction. '''
    for i in range(const.NUM_PLAYERS):
        # TODO find the most likely Wolf and only vote for that one
        if prediction[i] == 'Wolf':
            return i

    # TODO There are some really complicated game mechanics for the Minion.
    # https://boardgamegeek.com/thread/1422062/pointing-center-free-parking
    return (ind + 1) % const.NUM_PLAYERS
