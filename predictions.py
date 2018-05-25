import const
from const import logger
from copy import deepcopy
import random

def make_predictions(solution):
    '''
    Uses a list of true/false statements and possible role sets
    to return a list of predictions for all roles
    '''
    switch_dict = get_switch_dict(solution)
    curr_role_counts = dict(const.ROLE_COUNTS)
    all_role_guesses = get_basic_guesses(solution, curr_role_counts)

    solved = recurse_assign(solution, list(all_role_guesses), dict(curr_role_counts))
    if not solved:
        for j in range(len(all_role_guesses)):
            if all_role_guesses[j] == 'Wolf':
                all_role_guesses[j] = ''
                curr_role_counts['Wolf'] += 1
        solved = recurse_assign(solution, list(all_role_guesses), dict(curr_role_counts))

    final_guesses = [solved[switch_dict[i]] for i in range(len(solved))]
    return final_guesses

def get_basic_guesses(solution, curr_role_counts):
    all_role_guesses = []
    consistent_statements = solution.path
    consistent_roles = deepcopy(solution.possible_roles)
    for j in range(const.NUM_ROLES):
        guess_set = consistent_roles[j]
        if j >= len(consistent_statements) or consistent_statements[j]:     # Center card or Player is telling the truth
            for r in const.ROLE_SET:                                        # Remove already chosen cards
                if curr_role_counts[r] == 0:
                    guess_set -= set([r])

            if len(guess_set) == 1:                 # Player is telling the truth
                role = next(iter(guess_set))
                curr_role_counts[role] -= 1
                all_role_guesses.append(role)
            else:
                all_role_guesses.append('')

        elif not consistent_statements[j]:          # Player is lying
#            if curr_role_counts['Wolf'] > 0:
            all_role_guesses.append('Wolf')
            curr_role_counts['Wolf'] -= 1
#            else:                                   # TODO Robber stole from a Wolf!
#                all_role_guesses.append('')
#                for i in range(len(all_role_guesses)):
#                    if all_role_guesses[i] == 'Robber':
#                        all_role_guesses[i] = 'Wolf'
#                        curr_role_counts['Robber'] += 1
    return all_role_guesses

def recurse_assign(solution, all_role_guesses, curr_role_counts):
    ''' Assign the remaining unknown cards by recursing and finding a consistent placement. '''
    found = True
    for i in range(const.NUM_ROLES):
        if all_role_guesses[i] == '': found = False
    if found: return all_role_guesses

    for i in range(const.NUM_ROLES):
        if all_role_guesses[i] == '':
            leftover_roles = list(solution.possible_roles[i])
            random.shuffle(leftover_roles)
            for r in leftover_roles:
                if curr_role_counts[r] > 0:
                    curr_role_counts[r] -= 1
                    all_role_guesses[i] = r
                    result = recurse_assign(solution, list(all_role_guesses), dict(curr_role_counts))
                    if result: return result
                    curr_role_counts[r] += 1
                    all_role_guesses[i] = ''
    return False

def get_switch_dict(solution):
    switch_dict = {i:i for i in range(const.NUM_ROLES)}
    switches = sorted(solution.switches, key=lambda x: x[0])
    for priority, i, j in switches:
        temp = switch_dict[i]
        switch_dict[i] = switch_dict[j]
        switch_dict[j] = temp
    return switch_dict

def print_guesses(all_role_guesses):
    logger.info("\n[Wolfbot] Role guesses: " + str(all_role_guesses[:const.NUM_PLAYERS]) +
                "\n\t  Center cards: " + str(all_role_guesses[const.NUM_PLAYERS:]) + '\n')
