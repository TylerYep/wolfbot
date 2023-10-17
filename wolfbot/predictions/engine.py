import random

from wolfbot import const
from wolfbot.enums import Role
from wolfbot.solvers import SolverState


def get_basic_guesses(solution: SolverState) -> tuple[list[Role], dict[Role, int]]:
    """
    Populates the basic set of predictions, or adds the empty string if the
    possible roles set is not of size 1. For each statement, take the
    intersection and update the role counts for each character.

    Returns mutable objects because they are immediately used in recurse_assign().
    """
    if len(solution.possible_roles) != const.NUM_ROLES:
        raise RuntimeError("Solution is invalid.")

    all_role_guesses = []
    curr_role_counts = dict(const.ROLE_COUNTS)
    for j in range(const.NUM_ROLES):
        # Center card or is truth
        if j >= len(solution.path) or solution.path[j]:
            # Remove already chosen cards
            guess_set = {
                rol for rol in solution.possible_roles[j] if curr_role_counts[rol] > 0
            }

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
            # TODO: this has room for improvement.
            choice = Role.NONE
            for role in evil_roles:
                if curr_role_counts[role] > 0:
                    choice = role
                    break
            all_role_guesses.append(choice)
            if choice is not Role.NONE:
                curr_role_counts[choice] -= 1

    return all_role_guesses, curr_role_counts


def recurse_assign(
    solution: SolverState,
    all_role_guesses: list[Role],
    curr_role_counts: dict[Role, int],
    restrict_possible: bool = True,
) -> list[Role]:
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


def get_switch_dict(solution: SolverState) -> dict[int, int]:
    """
    Converts array of switches into a dictionary to index with.
    Sorts by priority before iterating.
    """
    switch_dict = {i: i for i in range(const.NUM_ROLES)}
    switches = sorted(solution.switches, key=lambda x: x[0])
    for _, i, j in switches:
        switch_dict[i], switch_dict[j] = switch_dict[j], switch_dict[i]
    return switch_dict
