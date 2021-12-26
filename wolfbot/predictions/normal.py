import random

from wolfbot import const
from wolfbot.const import Role
from wolfbot.predictions.engine import (
    get_basic_guesses,
    get_switch_dict,
    recurse_assign,
)
from wolfbot.predictions.evil import make_evil_prediction
from wolfbot.solvers import SolverState


def make_prediction(
    solution_arr: tuple[SolverState, ...], is_evil: bool = False
) -> tuple[Role, ...]:
    """
    Uses a list of true/false statements and possible role sets
    to return a list of predictions for all roles.
    """
    # This case only occurs when Wolves tell a perfect lie.
    if is_evil or not solution_arr:
        return make_evil_prediction(solution_arr)

    solutions_lst = list(solution_arr)
    random.shuffle(solutions_lst)
    solution_arr = tuple(solutions_lst)

    solved: list[Role] = []
    solution_index = 0
    for index, solution in enumerate(solution_arr):
        solution_index = index
        all_role_guesses, curr_role_counts = get_basic_guesses(solution)
        if solved := recurse_assign(solution, all_role_guesses, curr_role_counts):
            break

    # Assume all players that could lie are lying.
    if not solved:
        for index, solution in enumerate(solution_arr):
            solution_index = index
            all_role_guesses, curr_role_counts = get_basic_guesses(solution)
            if solved := recurse_assign(
                solution, all_role_guesses, curr_role_counts, restrict_possible=False
            ):
                break

    switch_dict = get_switch_dict(solution_arr[solution_index])
    final_guesses = tuple(solved[switch_dict[i]] for i in range(len(solved)))
    if len(final_guesses) != const.NUM_ROLES:
        raise RuntimeError("Could not find consistent assignment of roles.")
    return final_guesses
