""" solverstates.py """
from typing import FrozenSet, List, Set, Tuple

import pytest

from src import const
from src.algorithms import SolverState
from src.const import Priority


def create_frozen_sets(possible_roles: List[Set[str]]) -> Tuple[FrozenSet[str], ...]:
    """ Casts all sets in the list to frozen sets. """
    return tuple([frozenset(roles) for roles in possible_roles])


@pytest.fixture
def example_small_solverstate(small_game_roles: Tuple[str, ...]) -> SolverState:
    possible_roles = [{"Seer"}, {"Robber", "Villager", "Seer"}, {"Robber"}]

    return SolverState(
        create_frozen_sets(possible_roles),
        ((Priority.ROBBER, 2, 0),),
        (True,),
        role_counts={"Villager": 1, "Seer": 0, "Robber": 0},
    )


@pytest.fixture
def example_small_solverstate_solved(small_game_roles: Tuple[str, ...]) -> SolverState:
    possible_roles = [{"Villager"}, {"Robber"}, {"Seer"}]
    return SolverState(
        create_frozen_sets(possible_roles), ((Priority.ROBBER, 1, 2),), (True, True, True)
    )


@pytest.fixture
def example_medium_solverstate(medium_game_roles: Tuple[str, ...]) -> SolverState:
    possible_roles = [
        {"Seer"},
        {"Troublemaker", "Wolf", "Drunk", "Robber", "Seer", "Minion"},
        {"Drunk"},
        {"Troublemaker", "Wolf", "Drunk", "Robber", "Seer", "Minion"},
        {"Troublemaker", "Wolf", "Drunk", "Robber", "Seer", "Minion"},
        {"Troublemaker", "Wolf", "Drunk", "Robber", "Seer", "Minion"},
    ]
    return SolverState(create_frozen_sets(possible_roles), ((Priority.DRUNK, 2, 5),), (True, True))


@pytest.fixture
def example_medium_solverstate_solved(medium_game_roles: Tuple[str, ...]) -> SolverState:
    possible_roles = [
        {"Seer"},
        {"Robber", "Drunk", "Wolf", "Troublemaker", "Minion"},
        {"Drunk"},
        {"Robber"},
        {"Robber", "Drunk", "Wolf", "Troublemaker", "Minion"},
        {"Drunk", "Robber", "Seer", "Wolf", "Troublemaker", "Minion"},
    ]
    switches = ((Priority.DRUNK, 2, 5), (Priority.ROBBER, 3, 2))
    path = (True, False, True, True, False)
    return SolverState(create_frozen_sets(possible_roles), switches, path)


@pytest.fixture
def example_medium_solved_list(medium_game_roles: Tuple[str, ...]) -> List[SolverState]:
    possible_roles_1 = [
        {"Seer"},
        {"Robber", "Troublemaker", "Wolf", "Drunk", "Minion"},
        {"Drunk"},
        {"Robber"},
        {"Robber", "Troublemaker", "Wolf", "Drunk", "Minion"},
        {"Robber", "Troublemaker", "Wolf", "Drunk", "Seer", "Minion"},
    ]
    possible_roles_2 = [
        {"Robber", "Troublemaker", "Wolf", "Drunk", "Minion"},
        {"Wolf"},
        {"Drunk"},
        {"Robber"},
        {"Seer"},
        {"Robber", "Troublemaker", "Wolf", "Drunk", "Seer", "Minion"},
    ]
    return [
        SolverState(
            create_frozen_sets(possible_roles_1),
            ((Priority.DRUNK, 2, 5), (Priority.ROBBER, 3, 2)),
            (True, False, True, True, False),
        ),
        SolverState(
            create_frozen_sets(possible_roles_2),
            ((Priority.DRUNK, 2, 5), (Priority.ROBBER, 3, 2)),
            (False, False, True, True, True),
        ),
    ]


@pytest.fixture
def example_medium_solverstate_list(medium_game_roles: Tuple[str, ...]) -> List[SolverState]:
    possible_roles_1 = [
        {"Seer"},
        {"Robber"},
        {"Drunk"},
        {"Minion", "Wolf", "Seer", "Drunk", "Troublemaker"},
        {"Minion", "Wolf", "Drunk", "Troublemaker", "Robber"},
        {"Minion", "Wolf", "Seer", "Drunk", "Troublemaker", "Robber"},
    ]
    possible_roles_2 = [
        {"Seer"},
        {"Minion", "Wolf", "Seer", "Drunk", "Troublemaker"},
        {"Drunk"},
        {"Robber"},
        {"Minion", "Wolf", "Drunk", "Troublemaker", "Robber"},
        {"Minion", "Wolf", "Seer", "Drunk", "Troublemaker", "Robber"},
    ]
    possible_roles_3 = [
        {"Minion", "Wolf", "Drunk", "Troublemaker", "Robber"},
        {"Minion", "Wolf", "Seer", "Drunk", "Troublemaker"},
        {"Drunk"},
        {"Robber"},
        {"Seer"},
        {"Minion", "Wolf", "Seer", "Drunk", "Troublemaker", "Robber"},
    ]
    return [
        SolverState(
            create_frozen_sets(possible_roles_1),
            ((Priority.ROBBER, 1, 0), (Priority.DRUNK, 2, 5)),
            (True, True, True, False, False),
        ),
        SolverState(
            create_frozen_sets(possible_roles_2),
            ((Priority.DRUNK, 2, 5), (Priority.ROBBER, 3, 2)),
            (True, False, True, True, False),
        ),
        SolverState(
            create_frozen_sets(possible_roles_3),
            ((Priority.DRUNK, 2, 5), (Priority.ROBBER, 3, 2)),
            (False, False, True, True, True),
        ),
    ]


@pytest.fixture
def example_large_solverstate(large_game_roles: Tuple[str, ...]) -> SolverState:
    possible_roles = [
        {"Robber"},
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
        },
        {"Seer"},
        {"Villager"},
        {"Mason"},
        {"Mason"},
        {"Drunk"},
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
        },
    ] + [set(const.ROLE_SET)] * 7
    switches = ((Priority.ROBBER, 6, 0), (Priority.ROBBER, 9, 6))
    path = (True, False, True, True, True, True, True, False)
    return SolverState(create_frozen_sets(possible_roles), switches, path)
