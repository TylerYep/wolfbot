import random
from collections.abc import Callable
from pprint import pformat
from typing import TYPE_CHECKING, cast

from wolfbot import const
from wolfbot.enums import Role
from wolfbot.log import logger
from wolfbot.predictions.engine import get_basic_guesses, get_switch_dict
from wolfbot.predictions.evil import make_evil_prediction
from wolfbot.solvers import SolverState

if TYPE_CHECKING:
    from wolfbot.util import SupportsLessThan


def get_probs(solution_arr: tuple[SolverState, ...]) -> tuple[dict[Role, float], ...]:
    """
    Combines all solutions to create a probability distribution for the
    possible roles at each index.
    """
    result: tuple[dict[Role, float], ...] = tuple(
        dict.fromkeys(const.ROLE_SET, 0) for _ in range(const.NUM_ROLES)
    )
    for solution in solution_arr:
        for i, possible_roles_arr in enumerate(solution.possible_roles):
            this_dict = result[i]
            for option in possible_roles_arr:
                if option not in this_dict:
                    this_dict[option] = 0
                this_dict[option] += 1
            denom = sum(this_dict.values())
            for option in this_dict:
                this_dict[option] /= denom
    return result


def log_probability_dist(solution_probs: tuple[dict[Role, float], ...]) -> None:
    """
    Logs probability distributions from solutions.
    If the distribution is uniform, condenses it into a single 'All' key.
    If the distibution only has one nonzero value, only prints that value.
    Else prints all results as a dict.
    """
    results = {}
    for index, probs in enumerate(solution_probs):
        prob_values = set(probs.values())
        if len(prob_values) == 1:
            results[index] = {cast(Role, "ALL"): round(next(iter(prob_values)), 3)}
        elif len(prob_values) == 2:
            results[index] = {
                role: round(score, 3) for role, score in probs.items() if score > 0
            }
        else:
            results[index] = {role: round(score, 3) for role, score in probs.items()}
    logger.debug(pformat(results))


def make_relaxed_prediction(
    solution_arr: tuple[SolverState, ...],
    is_evil: bool = False,
    player_index: int | None = None,
) -> tuple[Role, ...]:
    """
    Uses a list of true/false statements and possible role sets
    to return a list of predictions for all roles.
    """
    # This case only occurs when Wolves tell a perfect lie.
    if is_evil or not solution_arr:
        return make_evil_prediction(solution_arr)

    solution_arr = tuple(
        sorted(solution_arr, key=lambda state: state.count_true, reverse=True)
    )
    solution_probs = get_probs(solution_arr)

    if player_index is not None and player_index == 0:
        log_probability_dist(solution_probs)

    solved_counts: dict[tuple[Role, ...], tuple[int, SolverState]] = {}
    for solution in solution_arr:
        all_role_guesses, curr_role_counts = get_basic_guesses(solution)
        if result := tuple(
            prob_recurse_assign(solution_probs, all_role_guesses, curr_role_counts)
        ):
            if result not in solved_counts:
                solved_counts[result] = (0, solution)
            solved_counts[result] = (
                solved_counts[result][0] + 1,
                solved_counts[result][1],
            )

    solved = max(solved_counts, key=lambda x: solved_counts[x][0])
    _, majority_solution = solved_counts[solved]
    switch_dict = get_switch_dict(majority_solution)
    final_guesses = tuple(solved[switch_dict[i]] for i in range(len(solved)))
    if len(final_guesses) != const.NUM_ROLES:
        raise RuntimeError("Could not find consistent assignment of roles.")
    return final_guesses


def prob_recurse_assign(
    solution_probs: tuple[dict[Role, float], ...],
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
        if all_role_guesses[i] is not Role.NONE:
            continue

        if restrict_possible:
            probs = solution_probs[i]
            leftover_roles = sorted(
                probs,
                key=cast(Callable[[Role], "SupportsLessThan"], probs.get),
                reverse=True,
            )
        else:
            leftover_roles = sorted(k for k, v in curr_role_counts.items() if v > 0)
            random.shuffle(leftover_roles)

        for rol in leftover_roles:
            if curr_role_counts[rol] > 0:
                curr_role_counts[rol] -= 1
                all_role_guesses[i] = rol
                if result := prob_recurse_assign(
                    solution_probs,
                    all_role_guesses,
                    curr_role_counts,
                    restrict_possible,
                ):
                    return result
                curr_role_counts[rol] += 1
                all_role_guesses[i] = Role.NONE
    # Unable to assign all roles
    return []
