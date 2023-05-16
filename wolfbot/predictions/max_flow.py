from pprint import pformat
from typing import cast

from cs.algorithms.graph.ford_fulkerson import ford_max_flow_network
from cs.structures.graph import Graph

from wolfbot import const
from wolfbot.enums import Role
from wolfbot.log import logger
from wolfbot.predictions.engine import get_switch_dict
from wolfbot.predictions.evil import make_evil_prediction
from wolfbot.solvers import SolverState


def get_probs(solution_arr: tuple[SolverState, ...]) -> tuple[dict[Role, float], ...]:
    """
    Combines all solutions to create a probability distribution for the
    possible roles at each index.
    """
    result: tuple[dict[Role, float], ...] = tuple(
        {role: 0 for role in const.ROLE_SET} for _ in range(const.NUM_ROLES)
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
        # Incorrectly assume lying players are always one of EVIL_ROLES
        # if i <= const.NUM_PLAYERS and not solution.path[i]:
        #     for role in const.EVIL_ROLES:
        #         this_dict[role] += 0.5
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


def make_max_flow_prediction(
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
        if result := tuple(max_flow_assign(solution_probs)):
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


def max_flow_assign(solution_probs: tuple[dict[Role, float], ...]) -> list[Role]:
    graph = Graph[str | int]()
    graph.add_node("Source")
    graph.add_node("Sink")
    for role in const.SORTED_ROLE_SET:
        graph.add_node(role.value)
        graph.add_edge("Source", role.value, weight=const.ROLE_COUNTS[role])
    for i in range(const.NUM_ROLES):
        graph.add_node(i)
        graph.add_edge(i, "Sink")
    for i, solution in enumerate(solution_probs):
        for role, prob in solution.items():
            if prob > 0:
                graph.add_edge(role.value, i)

    max_flow_graph = ford_max_flow_network(graph, "Source", "Sink")
    assert (
        sum(edge["flow"] for edge in max_flow_graph["Source"].values())
        == const.NUM_ROLES
    )
    result = [Role.NONE] * const.NUM_ROLES
    for edge in max_flow_graph.edges:
        if isinstance(edge.end, int) and edge["flow"] >= 1:
            result[edge.end] = Role(edge.start)
    return result
