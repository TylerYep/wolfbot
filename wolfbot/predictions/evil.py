import random

from wolfbot import const
from wolfbot.enums import Role
from wolfbot.predictions.engine import (
    get_basic_guesses,
    get_switch_dict,
    recurse_assign,
)
from wolfbot.solvers import SolverState


def make_random_prediction() -> tuple[Role, ...]:
    """Makes a random prediction."""
    random_guesses = list(const.ROLES)
    random.shuffle(random_guesses)
    return tuple(random_guesses)


def make_evil_prediction(solution_arr: tuple[SolverState, ...]) -> tuple[Role, ...]:
    """
    Makes the Wolf character's prediction for the game.
    """
    # TODO: Find better than random solution when the
    # Wolf gets contradicted by a later statement.
    if not solution_arr:
        return make_random_prediction()

    solution = random.choice(solution_arr)
    return make_unrestricted_prediction(solution)


def make_unrestricted_prediction(solution: SolverState) -> tuple[Role, ...]:
    """
    Uses a list of true/false statements and possible role sets
    to return a rushed list of predictions for all roles.
    Does not restrict guesses to the possible sets.
    """
    all_role_guesses, curr_role_counts = get_basic_guesses(solution)
    solved = recurse_assign(solution, all_role_guesses, curr_role_counts, False)
    switch_dict = get_switch_dict(solution)
    final_guesses = tuple(solved[switch_dict[i]] for i in range(len(solved)))
    if len(final_guesses) != const.NUM_ROLES:
        raise RuntimeError("Could not find unrestricted assignment of roles.")
    return final_guesses
