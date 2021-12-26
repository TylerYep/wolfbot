""" solverstates.py """
import pytest

from wolfbot import const
from wolfbot.enums import Role, SwitchPriority
from wolfbot.solvers import SolverState


@pytest.fixture
def example_small_solverstate(small_game_roles: tuple[Role, ...]) -> SolverState:
    possible_roles = (
        frozenset({Role.SEER}),
        frozenset({Role.ROBBER, Role.VILLAGER, Role.SEER}),
        frozenset({Role.ROBBER}),
    )
    return SolverState(
        possible_roles,
        ((SwitchPriority.ROBBER, 2, 0),),
        (True,),
        role_counts={Role.VILLAGER: 1, Role.SEER: 0, Role.ROBBER: 0},
    )


@pytest.fixture
def example_small_solverstate_solved(small_game_roles: tuple[Role, ...]) -> SolverState:
    possible_roles = (
        frozenset({Role.VILLAGER}),
        frozenset({Role.ROBBER}),
        frozenset({Role.SEER}),
    )
    return SolverState(
        possible_roles, ((SwitchPriority.ROBBER, 1, 2),), (True, True, True)
    )


@pytest.fixture
def example_medium_solverstate(medium_game_roles: tuple[Role, ...]) -> SolverState:
    possible_roles = (
        frozenset({Role.SEER}),
        frozenset(
            {
                Role.TROUBLEMAKER,
                Role.WOLF,
                Role.DRUNK,
                Role.ROBBER,
                Role.SEER,
                Role.MINION,
            }
        ),
        frozenset({Role.DRUNK}),
        frozenset(
            {
                Role.TROUBLEMAKER,
                Role.WOLF,
                Role.DRUNK,
                Role.ROBBER,
                Role.SEER,
                Role.MINION,
            }
        ),
        frozenset(
            {
                Role.TROUBLEMAKER,
                Role.WOLF,
                Role.DRUNK,
                Role.ROBBER,
                Role.SEER,
                Role.MINION,
            }
        ),
        frozenset(
            {
                Role.TROUBLEMAKER,
                Role.WOLF,
                Role.DRUNK,
                Role.ROBBER,
                Role.SEER,
                Role.MINION,
            }
        ),
    )
    return SolverState(possible_roles, ((SwitchPriority.DRUNK, 2, 5),), (True, True))


@pytest.fixture
def example_medium_solverstate_solved(
    medium_game_roles: tuple[Role, ...]
) -> SolverState:
    possible_roles = (
        frozenset({Role.SEER}),
        frozenset({Role.ROBBER, Role.DRUNK, Role.WOLF, Role.TROUBLEMAKER, Role.MINION}),
        frozenset({Role.DRUNK}),
        frozenset({Role.ROBBER}),
        frozenset({Role.ROBBER, Role.DRUNK, Role.WOLF, Role.TROUBLEMAKER, Role.MINION}),
        frozenset(
            {
                Role.DRUNK,
                Role.ROBBER,
                Role.SEER,
                Role.WOLF,
                Role.TROUBLEMAKER,
                Role.MINION,
            }
        ),
    )
    switches = ((SwitchPriority.DRUNK, 2, 5), (SwitchPriority.ROBBER, 3, 2))
    path = (True, False, True, True, False)
    return SolverState(possible_roles, switches, path)


@pytest.fixture
def example_medium_solved_list(
    medium_game_roles: tuple[Role, ...]
) -> tuple[SolverState, ...]:
    possible_roles_1 = (
        frozenset({Role.SEER}),
        frozenset({Role.ROBBER, Role.TROUBLEMAKER, Role.WOLF, Role.DRUNK, Role.MINION}),
        frozenset({Role.DRUNK}),
        frozenset({Role.ROBBER}),
        frozenset({Role.ROBBER, Role.TROUBLEMAKER, Role.WOLF, Role.DRUNK, Role.MINION}),
        frozenset(
            {
                Role.ROBBER,
                Role.TROUBLEMAKER,
                Role.WOLF,
                Role.DRUNK,
                Role.SEER,
                Role.MINION,
            }
        ),
    )
    possible_roles_2 = (
        frozenset({Role.ROBBER, Role.TROUBLEMAKER, Role.WOLF, Role.DRUNK, Role.MINION}),
        frozenset({Role.WOLF}),
        frozenset({Role.DRUNK}),
        frozenset({Role.ROBBER}),
        frozenset({Role.SEER}),
        frozenset(
            {
                Role.ROBBER,
                Role.TROUBLEMAKER,
                Role.WOLF,
                Role.DRUNK,
                Role.SEER,
                Role.MINION,
            }
        ),
    )
    return (
        SolverState(
            possible_roles_1,
            ((SwitchPriority.DRUNK, 2, 5), (SwitchPriority.ROBBER, 3, 2)),
            (True, False, True, True, False),
        ),
        SolverState(
            possible_roles_2,
            ((SwitchPriority.DRUNK, 2, 5), (SwitchPriority.ROBBER, 3, 2)),
            (False, False, True, True, True),
        ),
    )


@pytest.fixture
def example_medium_solverstate_list(
    medium_game_roles: tuple[Role, ...]
) -> tuple[SolverState, ...]:
    possible_roles_1 = (
        frozenset({Role.SEER}),
        frozenset({Role.ROBBER}),
        frozenset({Role.DRUNK}),
        frozenset({Role.MINION, Role.WOLF, Role.SEER, Role.DRUNK, Role.TROUBLEMAKER}),
        frozenset({Role.MINION, Role.WOLF, Role.DRUNK, Role.TROUBLEMAKER, Role.ROBBER}),
        frozenset(
            {
                Role.MINION,
                Role.WOLF,
                Role.SEER,
                Role.DRUNK,
                Role.TROUBLEMAKER,
                Role.ROBBER,
            }
        ),
    )
    possible_roles_2 = (
        frozenset({Role.SEER}),
        frozenset({Role.MINION, Role.WOLF, Role.SEER, Role.DRUNK, Role.TROUBLEMAKER}),
        frozenset({Role.DRUNK}),
        frozenset({Role.ROBBER}),
        frozenset({Role.MINION, Role.WOLF, Role.DRUNK, Role.TROUBLEMAKER, Role.ROBBER}),
        frozenset(
            {
                Role.MINION,
                Role.WOLF,
                Role.SEER,
                Role.DRUNK,
                Role.TROUBLEMAKER,
                Role.ROBBER,
            }
        ),
    )
    possible_roles_3 = (
        frozenset({Role.MINION, Role.WOLF, Role.DRUNK, Role.TROUBLEMAKER, Role.ROBBER}),
        frozenset({Role.MINION, Role.WOLF, Role.SEER, Role.DRUNK, Role.TROUBLEMAKER}),
        frozenset({Role.DRUNK}),
        frozenset({Role.ROBBER}),
        frozenset({Role.SEER}),
        frozenset(
            {
                Role.MINION,
                Role.WOLF,
                Role.SEER,
                Role.DRUNK,
                Role.TROUBLEMAKER,
                Role.ROBBER,
            }
        ),
    )
    return (
        SolverState(
            possible_roles_1,
            ((SwitchPriority.ROBBER, 1, 0), (SwitchPriority.DRUNK, 2, 5)),
            (True, True, True, False, False),
        ),
        SolverState(
            possible_roles_2,
            ((SwitchPriority.DRUNK, 2, 5), (SwitchPriority.ROBBER, 3, 2)),
            (True, False, True, True, False),
        ),
        SolverState(
            possible_roles_3,
            ((SwitchPriority.DRUNK, 2, 5), (SwitchPriority.ROBBER, 3, 2)),
            (False, False, True, True, True),
        ),
    )


@pytest.fixture
def example_large_solverstate(large_game_roles: tuple[Role, ...]) -> SolverState:
    possible_roles = (
        frozenset({Role.ROBBER}),
        frozenset(
            {
                Role.SEER,
                Role.HUNTER,
                Role.DRUNK,
                Role.TANNER,
                Role.WOLF,
                Role.INSOMNIAC,
                Role.MASON,
                Role.MINION,
                Role.VILLAGER,
                Role.TROUBLEMAKER,
            }
        ),
        frozenset({Role.SEER}),
        frozenset({Role.VILLAGER}),
        frozenset({Role.MASON}),
        frozenset({Role.MASON}),
        frozenset({Role.DRUNK}),
        frozenset(
            {
                Role.SEER,
                Role.HUNTER,
                Role.DRUNK,
                Role.TANNER,
                Role.WOLF,
                Role.INSOMNIAC,
                Role.MASON,
                Role.MINION,
                Role.VILLAGER,
                Role.TROUBLEMAKER,
            }
        ),
    ) + (const.ROLE_SET,) * 7
    switches = ((SwitchPriority.ROBBER, 6, 0), (SwitchPriority.ROBBER, 9, 6))
    path = (True, False, True, True, True, True, True, False)
    return SolverState(possible_roles, switches, path)
