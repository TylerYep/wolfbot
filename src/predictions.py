""" predictions.py """
import random
from typing import Dict, List, Tuple

from src import const
from src.const import Role
from src.solvers import SolverState


def make_random_prediction() -> Tuple[Role, ...]:
    """ Makes a random prediction. """
    random_guesses = list(const.ROLES)
    random.shuffle(random_guesses)
    return tuple(random_guesses)


def make_evil_prediction(solution_arr: Tuple[SolverState, ...]) -> Tuple[Role, ...]:
    """
    Makes the Wolf character's prediction for the game.
    """
    # TODO Find better than random solution when the
    # Wolf gets contradicted by a later statement.
    if not solution_arr[0].path:
        return make_random_prediction()

    solution = random.choice(solution_arr)
    return make_unrestricted_prediction(solution)


def make_unrestricted_prediction(solution: SolverState) -> Tuple[Role, ...]:
    """
    Uses a list of true/false statements and possible role sets
    to return a rushed list of predictions for all roles.
    Does not restrict guesses to the possible sets.
    """
    # if len(solution.possible_roles) != const.NUM_ROLES:
    #     return []
    all_role_guesses, curr_role_counts = get_basic_guesses(solution)
    solved = recurse_assign(
        solution, list(all_role_guesses), dict(curr_role_counts), False
    )
    switch_dict = get_switch_dict(solution)
    final_guesses = [solved[switch_dict[i]] for i in range(len(solved))]
    if len(final_guesses) != const.NUM_ROLES:
        raise RuntimeError("Could not find unrestricted assignment of roles.")
    return tuple(final_guesses)


def make_prediction(
    solution_arr: Tuple[SolverState, ...], is_evil: bool = False
) -> Tuple[Role, ...]:
    """
    Uses a list of true/false statements and possible role sets
    to return a list of predictions for all roles.
    """
    if is_evil:
        return make_evil_prediction(solution_arr)

    solutions_lst = list(solution_arr)
    random.shuffle(solutions_lst)
    solution_arr = tuple(solutions_lst)

    solved: List[Role] = []
    solution_index = 0
    for index, solution in enumerate(solution_arr):
        # This case only occurs when Wolves tell a perfect lie.
        if len(solution.possible_roles) != const.NUM_ROLES:
            return make_random_prediction()
        solution_index = index
        all_role_guesses, curr_role_counts = get_basic_guesses(solution)
        if solved := recurse_assign(
            solution, list(all_role_guesses), dict(curr_role_counts)
        ):
            break

    # Assume all players that could lie are lying.
    if not solved:
        for index, solution in enumerate(solution_arr):
            solution_index = index
            all_role_guesses, curr_role_counts = get_basic_guesses(solution)
            if solved := recurse_assign(
                solution,
                list(all_role_guesses),
                dict(curr_role_counts),
                restrict_possible=False,
            ):
                break

    switch_dict = get_switch_dict(solution_arr[solution_index])
    final_guesses = [solved[switch_dict[i]] for i in range(len(solved))]
    if len(final_guesses) != const.NUM_ROLES:
        raise RuntimeError("Could not find consistent assignment of roles.")
    return tuple(final_guesses)


def get_basic_guesses(
    solution: SolverState,
) -> Tuple[Tuple[Role, ...], Dict[Role, int]]:
    """
    Populates the basic set of predictions, or adds the empty string if the
    possible roles set is not of size 1. For each statement, take the
    intersection and update the role counts for each character.
    """
    if len(solution.possible_roles) != const.NUM_ROLES:
        raise RuntimeError("Solution is invalid.")

    all_role_guesses = []
    curr_role_counts = dict(const.ROLE_COUNTS)
    for j in range(const.NUM_ROLES):
        # Center card or is truth
        if j >= len(solution.path) or solution.path[j]:
            guess_set = solution.possible_roles[j]
            # Remove already chosen cards
            for rol in const.ROLE_SET:
                if curr_role_counts[rol] == 0:
                    guess_set -= {rol}

            # Player is telling the truth
            if len(guess_set) == 1:
                [role] = guess_set
                curr_role_counts[role] -= 1
                all_role_guesses.append(role)
            else:
                all_role_guesses.append(Role.NONE)

        # Player is lying
        elif not solution.path[j]:
            evil_roles = sorted(const.EVIL_ROLES)
            random.shuffle(evil_roles)

            # Choose a random evil player to be the guess.
            # TODO this has room for improvement.
            choice = Role.NONE
            for role in evil_roles:
                if curr_role_counts[role] > 0:
                    choice = role
                    break
            all_role_guesses.append(choice)
            if choice is not Role.NONE:
                curr_role_counts[choice] -= 1

    return tuple(all_role_guesses), curr_role_counts


def recurse_assign(
    solution: SolverState,
    all_role_guesses: List[Role],
    curr_role_counts: Dict[Role, int],
    restrict_possible: bool = True,
) -> List[Role]:
    """
    Assign the remaining unknown cards by recursing and finding a consistent placement.
    If restrict_possible is enabled, then uses the possible_roles sets to assign.
    Else simply fills in slots with curr_role_counts.
    """
    if Role.NONE not in all_role_guesses:
        return all_role_guesses

    for i in range(const.NUM_ROLES):
        if all_role_guesses[i] is Role.NONE:
            # sorted() will convert possible_roles sets into a sorted list.
            leftover_roles = sorted(
                solution.possible_roles[i]
                if restrict_possible
                else [k for k, v in curr_role_counts.items() if v > 0]
            )
            random.shuffle(leftover_roles)
            for rol in leftover_roles:
                if curr_role_counts[rol] > 0:
                    curr_role_counts[rol] -= 1
                    all_role_guesses[i] = rol
                    if result := recurse_assign(
                        solution, all_role_guesses, curr_role_counts, restrict_possible
                    ):
                        return result
                    curr_role_counts[rol] += 1
                    all_role_guesses[i] = Role.NONE
    # Unable to assign all roles
    return []


def get_switch_dict(solution: SolverState) -> Dict[int, int]:
    """
    Converts array of switches into a dictionary to index with.
    Sorts by priority before iterating.
    """
    switch_dict = {i: i for i in range(const.NUM_ROLES)}
    switches = sorted(solution.switches, key=lambda x: x[0])
    for _, i, j in switches:
        switch_dict[i], switch_dict[j] = switch_dict[j], switch_dict[i]
    return switch_dict
