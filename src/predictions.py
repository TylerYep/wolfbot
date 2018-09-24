''' predictions.py '''
import random
from copy import deepcopy
from const import logger
import const

def make_evil_prediction(solution_arr):
    '''
    Makes the Wolf character's prediction for the game.
    '''
    # TODO Find better than random solution when the Wolf gets contradicted in a later statement.
    if not solution_arr[0].path:
        random_guesses = list(const.ROLES)
        random.shuffle(random_guesses)
        return random_guesses

    solution = random.choice(solution_arr)
    return make_prediction_fast(solution)

    # all_role_guesses, curr_role_counts = get_basic_guesses(solution)
    # solved = recurse_assign(solution, list(all_role_guesses), dict(curr_role_counts), False)
    #
    # switch_dict = get_switch_dict(solution)
    # final_guesses = [solved[switch_dict[i]] for i in range(len(solved))]
    # return final_guesses


def make_prediction_fast(solution):
    '''
    Uses a list of true/false statements and possible role sets
    to return a rushed list of predictions for all roles.
    Does not restrict guesses to the possible sets.
    '''
    all_role_guesses, curr_role_counts = get_basic_guesses(solution)
    solved = recurse_assign(solution, list(all_role_guesses), dict(curr_role_counts), False)
    switch_dict = get_switch_dict(solution)
    final_guesses = [solved[switch_dict[i]] for i in range(len(solved))]
    return final_guesses


def make_prediction(solution_arr, is_evil=False):
    '''
    Uses a list of true/false statements and possible role sets
    to return a list of predictions for all roles
    '''
    if is_evil: return make_evil_prediction(solution_arr)

    solved = None
    random.shuffle(solution_arr)
    for solution in solution_arr:
        assert len(solution.possible_roles) == const.NUM_ROLES
        all_role_guesses, curr_role_counts = get_basic_guesses(solution)
        solved = recurse_assign(solution, list(all_role_guesses), dict(curr_role_counts))
        if solved: break

    if not solved:
        for solution in solution_arr:
            all_role_guesses, curr_role_counts = get_basic_guesses(solution)
            for j in range(const.NUM_ROLES):
                for role in ['Wolf', 'Robber', 'Insomniac']:
                    if all_role_guesses[j] == role:
                        all_role_guesses[j] = ''
                        curr_role_counts[role] += 1
            solved = recurse_assign(solution, list(all_role_guesses), dict(curr_role_counts))
            if solved: break

    switch_dict = get_switch_dict(solution)
    final_guesses = [solved[switch_dict[i]] for i in range(len(solved))]
    return final_guesses


def get_basic_guesses(solution):
    '''
    Populates the basic set of predictions, or adds the empty string if the
    possible roles set is not of size 1. For each statement, take the
    intersection and update the role counts for each character.
    '''
    all_role_guesses = []
    consistent_statements = list(solution.path)
    consistent_roles = deepcopy(solution.possible_roles)
    curr_role_counts = dict(const.ROLE_COUNTS)
    for j in range(const.NUM_ROLES):
        guess_set = consistent_roles[j]
        if j >= len(consistent_statements) or consistent_statements[j]:  # Center card or is truth
            for rol in const.ROLE_SET:                                # Remove already chosen cards
                if curr_role_counts[rol] == 0:
                    guess_set -= set([rol])

            if len(guess_set) == 1:                 # Player is telling the truth
                role = next(iter(guess_set))
                curr_role_counts[role] -= 1
                all_role_guesses.append(role)
            else:
                all_role_guesses.append('')

        elif not consistent_statements[j]:          # Player is lying
            if curr_role_counts['Wolf'] > 0:
                all_role_guesses.append('Wolf')
                curr_role_counts['Wolf'] -= 1
            else:
                all_role_guesses.append('')
    return all_role_guesses, curr_role_counts


def recurse_assign(solution, all_role_guesses, curr_role_counts, restrict_possible=True):
    '''
    Assign the remaining unknown cards by recursing and finding a consistent placement.
    If restrict_possible is enabled, then uses the possible-roles sets to assign.
    '''
    found = True
    for i in range(const.NUM_ROLES):
        if all_role_guesses[i] == '': found = False
    if found: return all_role_guesses

    for i in range(const.NUM_ROLES):
        if all_role_guesses[i] == '':
            if restrict_possible: leftover_roles = list(solution.possible_roles[i])
            else: leftover_roles = [k for k, v in curr_role_counts.items() if v > 0]
            random.shuffle(leftover_roles)
            for rol in leftover_roles:
                if curr_role_counts[rol] > 0:
                    curr_role_counts[rol] -= 1
                    all_role_guesses[i] = rol
                    result = recurse_assign(solution, all_role_guesses,
                                            curr_role_counts, restrict_possible)
                    if result: return result
                    curr_role_counts[rol] += 1
                    all_role_guesses[i] = ''
    return False


def get_switch_dict(solution):
    ''' Converts array of switches into a dictionary to index with. '''
    switch_dict = {i: i for i in range(const.NUM_ROLES)}
    switches = sorted(solution.switches, key=lambda x: x[0])
    for _, i, j in switches:
        temp = switch_dict[i]
        switch_dict[i] = switch_dict[j]
        switch_dict[j] = temp
    return switch_dict


def print_guesses(role_guesses):
    ''' Formats guesses to console. '''
    logger.info('\n[Wolfbot] Role guesses: %s\n\t  Center cards: %s\n',
                str(role_guesses[:const.NUM_PLAYERS]), str(role_guesses[const.NUM_PLAYERS:]))
