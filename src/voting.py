''' voting.py '''
from statistics import GameResult
from collections import defaultdict
from util import find_all_player_indices
from predictions import make_prediction, print_guesses
from const import logger
import const

def consolidate_results(solver, ORIGINAL_ROLES, game_roles, player_objs, all_statements):
    ''' Consolidates results and returns final GameResult. '''
    if const.USE_VOTING:
        wolf_inds = find_all_player_indices(ORIGINAL_ROLES, 'Wolf')
        all_role_guesses_arr = []
        for i in range(const.NUM_PLAYERS):
            # Good player vs Bad player guesses
            # TODO when a wolf becomes good?
            all_solutions = solver(all_statements, i)
            is_evil = i in wolf_inds and player_objs[i].new_role == ''
            is_evil = is_evil or player_objs[i].new_role == 'Wolf'
            all_role_guesses_arr.append(make_prediction(all_solutions, is_evil))

        for prediction in all_role_guesses_arr:
            logger.log(const.logging.TRACE, 'Player prediction: %s', str(prediction))
        all_role_guesses, confidence = get_voting_result(all_role_guesses_arr)
        print_guesses(all_role_guesses)
        logger.debug('Confidence level: %s', str([float('{0:0.2f}'.format(n)) for n in confidence]))
        found_vote_wolf = get_most_likely_wolf(game_roles, all_role_guesses, confidence)
        return GameResult(game_roles, all_role_guesses, all_statements, wolf_inds, found_vote_wolf)

    all_solutions = solver(all_statements)
    for solution in all_solutions:
        logger.log(const.logging.TRACE, 'Solver interpretation: %s', str(solution.path))
    all_role_guesses = make_prediction(all_solutions)
    print_guesses(all_role_guesses)
    return GameResult(game_roles, all_role_guesses, all_statements, wolf_inds)


def get_most_likely_wolf(game_roles, all_role_guesses, confidence):
    ''' Creates confidence levels for each prediction and selects the most likely Wolf. '''
    wolf_inds = find_all_player_indices(all_role_guesses[:const.NUM_PLAYERS], 'Wolf')
    max_confidence = 0
    most_likely_wolf = None
    for i in wolf_inds:
        if confidence[i] > max_confidence:
            max_confidence = confidence[i]
            most_likely_wolf = i

    if most_likely_wolf is None:
        logger.info('No wolves were found.')
        final_wolf_inds = find_all_player_indices(game_roles[:const.NUM_PLAYERS], 'Wolf')
        if final_wolf_inds:
            logger.info('Player(s) %s was a Wolf!\n', str(final_wolf_inds))
            return False

        logger.info('That was correct!\n')
        return True

    logger.info('Player %d was chosen as a Wolf.\nPlayer %d was a %s!\n',
                most_likely_wolf, most_likely_wolf, game_roles[most_likely_wolf])
    return game_roles[most_likely_wolf] == 'Wolf'


def get_voting_result(all_role_guesses_arr):
    ''' Take most common role guess array as the final guess for that index. '''
    all_role_guesses, confidence = [], []
    guess_histogram = defaultdict(int)
    for prediction in all_role_guesses_arr:
        guess_histogram[tuple(prediction)] += 1
    all_role_guesses, _ = max(guess_histogram.items(), key=lambda x: x[1])

    for i in range(const.NUM_ROLES):
        role_dict = defaultdict(int)
        for prediction in all_role_guesses_arr:
            role_dict[prediction[i]] += 1
        count = max(role_dict.values())
        confidence.append(count / const.NUM_PLAYERS)
    return list(all_role_guesses), confidence


def get_voting_result_old(all_role_guesses_arr):
    ''' Take most common guess as the guess for that index. May accuse too many of each role. '''
    all_role_guesses, confidence = [], []
    for i in range(const.NUM_ROLES):
        role_dict = defaultdict(int)
        for prediction in all_role_guesses_arr:
            role_dict[prediction[i]] += 1
        role, count = max(role_dict.items(), key=lambda x: x[1])
        all_role_guesses.append(role)
        confidence.append(count / const.NUM_PLAYERS)
    return all_role_guesses, confidence
