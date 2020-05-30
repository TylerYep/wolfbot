""" solverstates.py """
from typing import List, Tuple

import pytest

from src import const
from src.algorithms import SolverState
from src.const import SwitchPriority


@pytest.fixture
def example_small_solverstate(small_game_roles: Tuple[str, ...]) -> SolverState:
    possible_roles = (
        frozenset({"Seer"}),
        frozenset({"Robber", "Villager", "Seer"}),
        frozenset({"Robber"}),
    )
    return SolverState(
        possible_roles,
        ((SwitchPriority.ROBBER, 2, 0),),
        (True,),
        role_counts={"Villager": 1, "Seer": 0, "Robber": 0},
    )


@pytest.fixture
def example_small_solverstate_solved(small_game_roles: Tuple[str, ...]) -> SolverState:
    possible_roles = (frozenset({"Villager"}), frozenset({"Robber"}), frozenset({"Seer"}))
    return SolverState(possible_roles, ((SwitchPriority.ROBBER, 1, 2),), (True, True, True))


@pytest.fixture
def example_medium_solverstate(medium_game_roles: Tuple[str, ...]) -> SolverState:
    possible_roles = (
        frozenset({"Seer"}),
        frozenset({"Troublemaker", "Wolf", "Drunk", "Robber", "Seer", "Minion"}),
        frozenset({"Drunk"}),
        frozenset({"Troublemaker", "Wolf", "Drunk", "Robber", "Seer", "Minion"}),
        frozenset({"Troublemaker", "Wolf", "Drunk", "Robber", "Seer", "Minion"}),
        frozenset({"Troublemaker", "Wolf", "Drunk", "Robber", "Seer", "Minion"}),
    )
    return SolverState(possible_roles, ((SwitchPriority.DRUNK, 2, 5),), (True, True))


@pytest.fixture
def example_medium_solverstate_solved(medium_game_roles: Tuple[str, ...]) -> SolverState:
    possible_roles = (
        frozenset({"Seer"}),
        frozenset({"Robber", "Drunk", "Wolf", "Troublemaker", "Minion"}),
        frozenset({"Drunk"}),
        frozenset({"Robber"}),
        frozenset({"Robber", "Drunk", "Wolf", "Troublemaker", "Minion"}),
        frozenset({"Drunk", "Robber", "Seer", "Wolf", "Troublemaker", "Minion"}),
    )
    switches = ((SwitchPriority.DRUNK, 2, 5), (SwitchPriority.ROBBER, 3, 2))
    path = (True, False, True, True, False)
    return SolverState(possible_roles, switches, path)


@pytest.fixture
def example_medium_solved_list(medium_game_roles: Tuple[str, ...]) -> List[SolverState]:
    possible_roles_1 = (
        frozenset({"Seer"}),
        frozenset({"Robber", "Troublemaker", "Wolf", "Drunk", "Minion"}),
        frozenset({"Drunk"}),
        frozenset({"Robber"}),
        frozenset({"Robber", "Troublemaker", "Wolf", "Drunk", "Minion"}),
        frozenset({"Robber", "Troublemaker", "Wolf", "Drunk", "Seer", "Minion"}),
    )
    possible_roles_2 = (
        frozenset({"Robber", "Troublemaker", "Wolf", "Drunk", "Minion"}),
        frozenset({"Wolf"}),
        frozenset({"Drunk"}),
        frozenset({"Robber"}),
        frozenset({"Seer"}),
        frozenset({"Robber", "Troublemaker", "Wolf", "Drunk", "Seer", "Minion"}),
    )
    return [
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
    ]


@pytest.fixture
def example_medium_solverstate_list(medium_game_roles: Tuple[str, ...]) -> List[SolverState]:
    possible_roles_1 = (
        frozenset({"Seer"}),
        frozenset({"Robber"}),
        frozenset({"Drunk"}),
        frozenset({"Minion", "Wolf", "Seer", "Drunk", "Troublemaker"}),
        frozenset({"Minion", "Wolf", "Drunk", "Troublemaker", "Robber"}),
        frozenset({"Minion", "Wolf", "Seer", "Drunk", "Troublemaker", "Robber"}),
    )
    possible_roles_2 = (
        frozenset({"Seer"}),
        frozenset({"Minion", "Wolf", "Seer", "Drunk", "Troublemaker"}),
        frozenset({"Drunk"}),
        frozenset({"Robber"}),
        frozenset({"Minion", "Wolf", "Drunk", "Troublemaker", "Robber"}),
        frozenset({"Minion", "Wolf", "Seer", "Drunk", "Troublemaker", "Robber"}),
    )
    possible_roles_3 = (
        frozenset({"Minion", "Wolf", "Drunk", "Troublemaker", "Robber"}),
        frozenset({"Minion", "Wolf", "Seer", "Drunk", "Troublemaker"}),
        frozenset({"Drunk"}),
        frozenset({"Robber"}),
        frozenset({"Seer"}),
        frozenset({"Minion", "Wolf", "Seer", "Drunk", "Troublemaker", "Robber"}),
    )
    return [
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
    ]


@pytest.fixture
def example_large_solverstate(large_game_roles: Tuple[str, ...]) -> SolverState:
    possible_roles = (
        frozenset({"Robber"}),
        frozenset(
            {
                "Seer",
                "Hunter",
                "Drunk",
                "Tanner",
                "Wolf",
                "Insomniac",
                "Mason",
                "Minion",
                "Villager",
                "Troublemaker",
            }
        ),
        frozenset({"Seer"}),
        frozenset({"Villager"}),
        frozenset({"Mason"}),
        frozenset({"Mason"}),
        frozenset({"Drunk"}),
        frozenset(
            {
                "Seer",
                "Hunter",
                "Drunk",
                "Tanner",
                "Wolf",
                "Insomniac",
                "Mason",
                "Minion",
                "Villager",
                "Troublemaker",
            }
        ),
    ) + (const.ROLE_SET,) * 7
    switches = ((SwitchPriority.ROBBER, 6, 0), (SwitchPriority.ROBBER, 9, 6))
    path = (True, False, True, True, True, True, True, False)
    return SolverState(possible_roles, switches, path)
