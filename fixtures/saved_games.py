""" savedgames.py """
# pylint: disable=missing-function-docstring
from typing import Tuple

import pytest

from src import const
from src.const import Role, RoleBits, SwitchPriority
from src.roles import Drunk, Hunter, Mason, Minion, Robber, Seer, Tanner, Villager, Wolf
from src.statements import Statement
from src.stats import SavedGame


@pytest.fixture
def example_small_saved_game(small_game_roles: Tuple[Role, ...]) -> SavedGame:
    return SavedGame(
        (Role.VILLAGER, Role.ROBBER, Role.SEER),
        (Role.VILLAGER, Role.SEER, Role.ROBBER),
        (
            Statement("I am a Villager.", ((0, RoleBits(Role.VILLAGER)),)),
            Statement(
                "I am a Robber and I swapped with Player 2. I am now a Seer.",
                ((1, RoleBits(Role.ROBBER)), (2, RoleBits(Role.SEER)),),
                ((SwitchPriority.ROBBER, 1, 2),),
            ),
            Statement(
                "I am a Seer and I saw that Player 1 was a Robber.",
                ((2, RoleBits(Role.SEER)), (1, RoleBits(Role.ROBBER)),),
            ),
        ),
        (Villager(0), Robber(1, 2, Role.SEER), Seer(2, (1, Role.ROBBER), (None, None))),
    )


@pytest.fixture
def example_medium_saved_game(medium_game_roles: Tuple[Role, ...]) -> SavedGame:
    return SavedGame(
        (Role.SEER, Role.WOLF, Role.DRUNK, Role.ROBBER, Role.MINION, Role.TROUBLEMAKER),
        (Role.SEER, Role.WOLF, Role.TROUBLEMAKER, Role.DRUNK, Role.MINION, Role.ROBBER),
        (
            Statement(
                "I am a Seer and I saw that Player 2 was a Drunk.",
                ((0, RoleBits(Role.SEER)), (2, RoleBits(Role.DRUNK)),),
            ),
            Statement(
                "I am a Robber and I swapped with Player 0. I am now a Seer.",
                ((1, RoleBits(Role.ROBBER)), (0, RoleBits(Role.SEER)),),
                ((SwitchPriority.ROBBER, 1, 0),),
            ),
            Statement(
                "I am a Drunk and I swapped with Center 0.",
                ((2, RoleBits(Role.DRUNK)),),
                ((SwitchPriority.DRUNK, 2, 5),),
            ),
            Statement(
                "I am a Robber and I swapped with Player 2. I am now a Drunk.",
                ((3, RoleBits(Role.ROBBER)), (2, RoleBits(Role.DRUNK)),),
                ((SwitchPriority.ROBBER, 3, 2),),
            ),
            Statement(
                "I am a Seer and I saw that Player 3 was a Robber.",
                ((4, RoleBits(Role.SEER)), (3, RoleBits(Role.ROBBER)),),
            ),
        ),
        (
            Seer(0, (2, Role.DRUNK)),
            Wolf(1, (1,), 5, Role.TROUBLEMAKER),
            Drunk(2, 5),
            Robber(3, 2, Role.DRUNK),
            Minion(4, (1,)),
        ),
    )


@pytest.fixture
def example_large_saved_game(large_game_roles: Tuple[Role, ...]) -> SavedGame:
    mason_roles = tuple([(i, ~RoleBits(Role.MASON)) for i in range(const.NUM_PLAYERS) if i != 2])
    return SavedGame(
        (
            Role.VILLAGER,
            Role.DRUNK,
            Role.MASON,
            Role.TANNER,
            Role.VILLAGER,
            Role.ROBBER,
            Role.SEER,
            Role.WOLF,
            Role.MINION,
            Role.VILLAGER,
            Role.WOLF,
            Role.HUNTER,
            Role.TROUBLEMAKER,
            Role.MASON,
            Role.INSOMNIAC,
        ),
        (
            Role.VILLAGER,
            Role.INSOMNIAC,
            Role.MASON,
            Role.TANNER,
            Role.VILLAGER,
            Role.DRUNK,
            Role.SEER,
            Role.WOLF,
            Role.MINION,
            Role.VILLAGER,
            Role.WOLF,
            Role.HUNTER,
            Role.TROUBLEMAKER,
            Role.MASON,
            Role.ROBBER,
        ),
        (
            Statement("I am a Villager.", ((0, RoleBits(Role.VILLAGER)),)),
            Statement(
                "I am a Drunk and I swapped with Center 2.",
                ((1, RoleBits(Role.DRUNK)),),
                ((SwitchPriority.DRUNK, 1, 14),),
            ),
            Statement(
                "I am a Mason. The other Mason is not present.",
                ((2, RoleBits(Role.MASON)),) + mason_roles,
            ),
            Statement(
                "I am a Robber and I swapped with Player 10. I am now a Insomniac.",
                ((3, RoleBits(Role.ROBBER)), (10, RoleBits(Role.INSOMNIAC)),),
                ((SwitchPriority.ROBBER, 3, 10),),
            ),
            Statement("I am a Villager.", ((4, RoleBits(Role.VILLAGER)),)),
            Statement(
                "I am a Robber and I swapped with Player 1. I am now a Drunk.",
                ((5, RoleBits(Role.ROBBER)), (1, RoleBits(Role.DRUNK)),),
                ((SwitchPriority.ROBBER, 5, 1),),
            ),
            Statement(
                (
                    "I am a Seer and I saw that Center 1 was a Mason and that "
                    "Center 0 was a Troublemaker."
                ),
                (
                    (6, RoleBits(Role.SEER)),
                    (13, RoleBits(Role.MASON)),
                    (12, RoleBits(Role.TROUBLEMAKER)),
                ),
            ),
            Statement(
                "I am a Seer and I saw that Player 3 was a Robber.",
                ((7, RoleBits(Role.SEER)), (3, RoleBits(Role.ROBBER)),),
            ),
            Statement(
                "I am a Troublemaker and I swapped Player 0 and Player 1.",
                ((8, RoleBits(Role.TROUBLEMAKER)),),
                ((SwitchPriority.TROUBLEMAKER, 0, 1),),
            ),
            Statement("I am a Villager.", ((9, RoleBits(Role.VILLAGER)),)),
            Statement(
                "I am a Troublemaker and I swapped Player 3 and Player 4.",
                ((10, RoleBits(Role.TROUBLEMAKER)),),
                ((SwitchPriority.TROUBLEMAKER, 3, 4),),
            ),
            Statement("I am a Hunter.", ((11, RoleBits(Role.HUNTER)),)),
        ),
        (
            Villager(0),
            Drunk(1, 14),
            Mason(2, (2,)),
            Tanner(3),
            Villager(4),
            Robber(5, 1, Role.DRUNK),
            Seer(6, (13, Role.MASON), (12, Role.TROUBLEMAKER)),
            Wolf(7, (7, 10), None, None),
            Minion(8, (7, 10)),
            Villager(9),
            Wolf(10, (7, 10), None, None),
            Hunter(11),
        ),
    )
