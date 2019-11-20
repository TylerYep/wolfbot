''' predictions.py '''
from typing import Dict, List, Tuple, Union
import random

from src.algorithms import SolverState
from src.roles.player import Player
from src.const import logger
from src import const

def make_random_prediction() -> List[str]:
    ''' Makes a random prediction. '''
    random_guesses = list(const.ROLES)
    random.shuffle(random_guesses)
    return random_guesses


def make_evil_prediction(solution_arr: List[SolverState]) -> List[str]:
    '''
    Makes the Wolf character's prediction for the game.
    '''
    # TODO Find better than random solution when the Wolf gets contradicted by a later statement.
    if not solution_arr[0].path:
        return make_random_prediction()

    solution = random.choice(solution_arr)
    return make_unrestricted_prediction(solution)


def make_unrestricted_prediction(solution: SolverState) -> List[str]:
    '''
    Uses a list of true/false statements and possible role sets
    to return a rushed list of predictions for all roles.
    Does not restrict guesses to the possible sets.
    '''
    if len(solution.possible_roles) != const.NUM_ROLES:
        return []
    all_role_guesses, curr_role_counts = get_basic_guesses(solution)
    solved = recurse_assign(solution, list(all_role_guesses), dict(curr_role_counts), False)
    switch_dict = get_switch_dict(solution)
    final_guesses = [solved[switch_dict[i]] for i in range(len(solved))]
    return final_guesses


def make_prediction(solution_arr: List[SolverState], is_evil: bool = False) -> List[str]:
    '''
    Uses a list of true/false statements and possible role sets
    to return a list of predictions for all roles.
    '''
    if is_evil:
        return make_evil_prediction(solution_arr)

    solved: List[str] = []
    solution_index = 0
    random.shuffle(solution_arr)
    for index, solution in enumerate(solution_arr):
        # This case only occurs when Wolves tell a perfect lie.
        if len(solution.possible_roles) != const.NUM_ROLES:
            return make_random_prediction()
        solution_index = index
        all_role_guesses, curr_role_counts = get_basic_guesses(solution)
        solved = recurse_assign(solution, list(all_role_guesses), dict(curr_role_counts))
        if solved: break

    if not solved:
        for index, solution in enumerate(solution_arr):
            solution_index = index
            all_role_guesses, curr_role_counts = get_basic_guesses(solution)
            for j in range(const.NUM_ROLES):
                for role in ('Wolf', 'Minion', 'Robber', 'Insomniac', 'Tanner'):
                    if all_role_guesses[j] == role:
                        all_role_guesses[j] = ''
                        curr_role_counts[role] += 1
            solved = recurse_assign(solution, list(all_role_guesses), dict(curr_role_counts))
            if solved: break

    if not solved:
        for index, solution in enumerate(solution_arr):
            solution_index = index
            solved = make_unrestricted_prediction(solution)
            if solved: break

    switch_dict = get_switch_dict(solution_arr[solution_index])
    final_guesses = [solved[switch_dict[i]] for i in range(len(solved))]
    assert len(final_guesses) == const.NUM_ROLES
    return final_guesses


def get_basic_guesses(solution: SolverState) -> Tuple[List[str], Dict[str, int]]:
    '''
    Populates the basic set of predictions, or adds the empty string if the
    possible roles set is not of size 1. For each statement, take the
    intersection and update the role counts for each character.
    '''
    assert len(solution.possible_roles) == const.NUM_ROLES

    all_role_guesses = []
    consistent_statements = list(solution.path)
    curr_role_counts = dict(const.ROLE_COUNTS)
    for j in range(const.NUM_ROLES):
        if j >= len(consistent_statements) or consistent_statements[j]:  # Center card or is truth
            guess_set = solution.possible_roles[j]
            for rol in const.ROLE_SET:              # Remove already chosen cards
                if curr_role_counts[rol] == 0:
                    guess_set -= set([rol])

            if len(guess_set) == 1:                 # Player is telling the truth
                [role] = guess_set
                curr_role_counts[role] -= 1
                all_role_guesses.append(role)
            else:
                all_role_guesses.append('')

        elif not consistent_statements[j]:          # Player is lying
            evil_roles = sorted(tuple(const.EVIL_ROLES))
            random.shuffle(evil_roles)
            choices = [r for r in evil_roles if curr_role_counts[r] > 0]
            if choices:
                choice = random.choice(choices)
                all_role_guesses.append(choice)
                curr_role_counts[choice] -= 1
            else:
                all_role_guesses.append('')
    return all_role_guesses, curr_role_counts


def recurse_assign(solution: SolverState,
                   all_role_guesses: List[str],
                   curr_role_counts: Dict[str, int],
                   restrict_possible: bool = True) -> List[str]:
    '''
    Assign the remaining unknown cards by recursing and finding a consistent placement.
    If restrict_possible is enabled, then uses the possible_roles sets to assign.
    Else simply fills in slots with curr_role_counts.
    '''
    if '' not in all_role_guesses:
        return all_role_guesses

    for i in range(const.NUM_ROLES):
        if all_role_guesses[i] == '':
            leftover_roles = sorted(solution.possible_roles[i] if restrict_possible \
                                else [k for k, v in curr_role_counts.items() if v > 0])
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
    # Unable to assign all roles
    return []


def get_switch_dict(solution: SolverState) -> Dict[int, int]:
    '''
    Converts array of switches into a dictionary to index with.
    Sorts by priority before iterating.
    '''
    switch_dict = {i: i for i in range(const.NUM_ROLES)}
    switches = sorted(solution.switches, key=lambda x: x[0])
    for _, i, j in switches:
        temp = switch_dict[i]
        switch_dict[i] = switch_dict[j]
        switch_dict[j] = temp
    return switch_dict


def print_guesses(role_guesses: Union[List[Player], List[str]]) -> None:
    ''' Formats guesses to console. '''
    logger.info((f'\n[Wolfbot] Role guesses: {role_guesses[:const.NUM_PLAYERS]}\n' + ' '*10 +
                 f'Center cards: {role_guesses[const.NUM_PLAYERS:]}\n').replace('\'', ''))
