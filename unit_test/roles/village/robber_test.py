""" robber_test.py """
from typing import Tuple

from conftest import set_roles
from src import const
from src.const import SwitchPriority
from src.roles import Robber
from src.statements import Statement


class TestRobber:
    """ Tests for the Robber player class. """

    @staticmethod
    def test_awake_init(large_game_roles: Tuple[str, ...]) -> None:
        """
        Should initialize a Robber. Note that the player_index of the Robber is not necessarily
        the index where the true Robber is located.
        """
        player_index = 2
        game_roles = list(large_game_roles)
        new_roles = list(large_game_roles)
        new_roles[2], new_roles[6] = new_roles[6], new_roles[2]

        expected = (
            Statement(
                "I am a Robber and I swapped with Player 6. I am now a Mason.",
                ((2, frozenset({"Robber"})), (6, frozenset({"Mason"}))),
                ((SwitchPriority.ROBBER, 2, 6),),
                "Robber",
            ),
        )

        robber = Robber.awake_init(player_index, game_roles, [])

        assert game_roles == new_roles
        assert robber.choice_ind == 6
        assert robber.new_role == "Mason"
        assert robber.statements == expected

    @staticmethod
    def test_get_robber_statements() -> None:
        """ Should execute initialization actions and return the possible statements. """
        player_index = 4

        result = Robber.get_robber_statements(player_index, 3, "Seer")

        assert result == (
            Statement(
                "I am a Robber and I swapped with Player 3. I am now a Seer.",
                ((4, frozenset({"Robber"})), (3, frozenset({"Seer"}))),
                ((SwitchPriority.ROBBER, 4, 3),),
                "Robber",
            ),
        )

    @staticmethod
    def test_get_all_statements() -> None:
        """ Should return the possible statements from all possible initialization actions. """
        player_index = 1
        set_roles("Wolf", "Robber", "Villager")
        const.NUM_PLAYERS = 2
        expected = (
            Statement(
                "I am a Robber and I swapped with Player 0. I am now a Villager.",
                ((1, frozenset({"Robber"})), (0, frozenset({"Villager"}))),
                ((SwitchPriority.ROBBER, 1, 0),),
                "Robber",
            ),
            Statement(
                "I am a Robber and I swapped with Player 0. I am now a Wolf.",
                ((1, frozenset({"Robber"})), (0, frozenset({"Wolf"}))),
                ((SwitchPriority.ROBBER, 1, 0),),
                "Robber",
            ),
            Statement(
                "I am a Robber and I swapped with Player 0. I am now a Robber.",
                ((1, frozenset({"Robber"})), (0, frozenset({"Robber"}))),
                ((SwitchPriority.ROBBER, 1, 0),),
                "Robber",
            ),
        )

        result = Robber.get_all_statements(player_index)

        assert set(result) == set(expected)
