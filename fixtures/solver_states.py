""" solverstates.py """
# pylint: disable=missing-function-docstring
from typing import Tuple

import pytest

from src import const
from src.const import Role, RoleBits, SwitchPriority
from src.solvers import SolverState


@pytest.fixture
def example_small_solverstate(small_game_roles: Tuple[Role, ...]) -> SolverState:
    possible_roles = (
        RoleBits.from_roles(Role.SEER),
        RoleBits.from_roles(Role.ROBBER, Role.VILLAGER, Role.SEER),
        RoleBits.from_roles(Role.ROBBER),
    )
    return SolverState(
        possible_roles,
        ((SwitchPriority.ROBBER, 2, 0),),
        (True,),
        role_counts={Role.VILLAGER: 1, Role.SEER: 0, Role.ROBBER: 0},
    )


@pytest.fixture
def example_small_solverstate_solved(small_game_roles: Tuple[Role, ...]) -> SolverState:
    possible_roles = (
        RoleBits.from_roles(Role.VILLAGER),
        RoleBits.from_roles(Role.ROBBER),
        RoleBits.from_roles(Role.SEER),
    )
    return SolverState(possible_roles, ((SwitchPriority.ROBBER, 1, 2),), (True, True, True))


@pytest.fixture
def example_medium_solverstate(medium_game_roles: Tuple[Role, ...]) -> SolverState:
    possible_roles = (
        RoleBits.from_roles(Role.SEER),
        RoleBits.from_roles(
            Role.TROUBLEMAKER, Role.WOLF, Role.DRUNK, Role.ROBBER, Role.SEER, Role.MINION
        ),
        RoleBits.from_roles(Role.DRUNK),
        RoleBits.from_roles(
            Role.TROUBLEMAKER, Role.WOLF, Role.DRUNK, Role.ROBBER, Role.SEER, Role.MINION
        ),
        RoleBits.from_roles(
            Role.TROUBLEMAKER, Role.WOLF, Role.DRUNK, Role.ROBBER, Role.SEER, Role.MINION
        ),
        RoleBits.from_roles(
            Role.TROUBLEMAKER, Role.WOLF, Role.DRUNK, Role.ROBBER, Role.SEER, Role.MINION
        ),
    )
    return SolverState(possible_roles, ((SwitchPriority.DRUNK, 2, 5),), (True, True))


@pytest.fixture
def example_medium_solverstate_solved(medium_game_roles: Tuple[Role, ...]) -> SolverState:
    possible_roles = (
        RoleBits.from_roles(Role.SEER),
        RoleBits.from_roles(Role.ROBBER, Role.DRUNK, Role.WOLF, Role.TROUBLEMAKER, Role.MINION),
        RoleBits.from_roles(Role.DRUNK),
        RoleBits.from_roles(Role.ROBBER),
        RoleBits.from_roles(Role.ROBBER, Role.DRUNK, Role.WOLF, Role.TROUBLEMAKER, Role.MINION),
        RoleBits.from_roles(
            Role.DRUNK, Role.ROBBER, Role.SEER, Role.WOLF, Role.TROUBLEMAKER, Role.MINION
        ),
    )
    switches = ((SwitchPriority.DRUNK, 2, 5), (SwitchPriority.ROBBER, 3, 2))
    path = (True, False, True, True, False)
    return SolverState(possible_roles, switches, path)


@pytest.fixture
def example_medium_solved_list(medium_game_roles: Tuple[Role, ...]) -> Tuple[SolverState, ...]:
    possible_roles_1 = (
        RoleBits.from_roles(Role.SEER),
        RoleBits.from_roles(Role.ROBBER, Role.TROUBLEMAKER, Role.WOLF, Role.DRUNK, Role.MINION),
        RoleBits.from_roles(Role.DRUNK),
        RoleBits.from_roles(Role.ROBBER),
        RoleBits.from_roles(Role.ROBBER, Role.TROUBLEMAKER, Role.WOLF, Role.DRUNK, Role.MINION),
        RoleBits.from_roles(
            Role.ROBBER, Role.TROUBLEMAKER, Role.WOLF, Role.DRUNK, Role.SEER, Role.MINION
        ),
    )
    possible_roles_2 = (
        RoleBits.from_roles(Role.ROBBER, Role.TROUBLEMAKER, Role.WOLF, Role.DRUNK, Role.MINION),
        RoleBits.from_roles(Role.WOLF),
        RoleBits.from_roles(Role.DRUNK),
        RoleBits.from_roles(Role.ROBBER),
        RoleBits.from_roles(Role.SEER),
        RoleBits.from_roles(
            Role.ROBBER, Role.TROUBLEMAKER, Role.WOLF, Role.DRUNK, Role.SEER, Role.MINION
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
def example_medium_solverstate_list(medium_game_roles: Tuple[Role, ...]) -> Tuple[SolverState, ...]:
    possible_roles_1 = (
        RoleBits.from_roles(Role.SEER),
        RoleBits.from_roles(Role.ROBBER),
        RoleBits.from_roles(Role.DRUNK),
        RoleBits.from_roles(Role.MINION, Role.WOLF, Role.SEER, Role.DRUNK, Role.TROUBLEMAKER),
        RoleBits.from_roles(Role.MINION, Role.WOLF, Role.DRUNK, Role.TROUBLEMAKER, Role.ROBBER),
        RoleBits.from_roles(
            Role.MINION, Role.WOLF, Role.SEER, Role.DRUNK, Role.TROUBLEMAKER, Role.ROBBER
        ),
    )
    possible_roles_2 = (
        RoleBits.from_roles(Role.SEER),
        RoleBits.from_roles(Role.MINION, Role.WOLF, Role.SEER, Role.DRUNK, Role.TROUBLEMAKER),
        RoleBits.from_roles(Role.DRUNK),
        RoleBits.from_roles(Role.ROBBER),
        RoleBits.from_roles(Role.MINION, Role.WOLF, Role.DRUNK, Role.TROUBLEMAKER, Role.ROBBER),
        RoleBits.from_roles(
            Role.MINION, Role.WOLF, Role.SEER, Role.DRUNK, Role.TROUBLEMAKER, Role.ROBBER
        ),
    )
    possible_roles_3 = (
        RoleBits.from_roles(Role.MINION, Role.WOLF, Role.DRUNK, Role.TROUBLEMAKER, Role.ROBBER),
        RoleBits.from_roles(Role.MINION, Role.WOLF, Role.SEER, Role.DRUNK, Role.TROUBLEMAKER),
        RoleBits.from_roles(Role.DRUNK),
        RoleBits.from_roles(Role.ROBBER),
        RoleBits.from_roles(Role.SEER),
        RoleBits.from_roles(
            Role.MINION, Role.WOLF, Role.SEER, Role.DRUNK, Role.TROUBLEMAKER, Role.ROBBER
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
def example_large_solverstate(large_game_roles: Tuple[Role, ...]) -> SolverState:
    possible_roles = (
        RoleBits.from_roles(Role.ROBBER),
        RoleBits.from_roles(
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
        ),
        RoleBits.from_roles(Role.SEER),
        RoleBits.from_roles(Role.VILLAGER),
        RoleBits.from_roles(Role.MASON),
        RoleBits.from_roles(Role.MASON),
        RoleBits.from_roles(Role.DRUNK),
        RoleBits.from_roles(
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
        ),
    ) + (RoleBits.from_role_bits(const.ROLE_BITSET),) * 7
    switches = ((SwitchPriority.ROBBER, 6, 0), (SwitchPriority.ROBBER, 9, 6))
    path = (True, False, True, True, True, True, True, False)
    return SolverState(possible_roles, switches, path)
