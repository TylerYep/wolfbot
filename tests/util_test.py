import pytest

from tests.conftest import verify_output_string
from wolfbot import util
from wolfbot.enums import Role


class TestPrintRoles:
    """Tests for the print_roles function."""

    @staticmethod
    def test_print_roles(
        caplog: pytest.LogCaptureFixture, small_game_roles: tuple[Role, ...]
    ) -> None:
        """Correctly print and format roles."""
        shuffled_roles = [Role.SEER, Role.VILLAGER, Role.WOLF, Role.ROBBER]

        util.print_roles(shuffled_roles, "Hidden")

        expected = (
            "[Hidden] Player roles: [Seer, Villager, Wolf]\n"
            f"{' ' * 9}Center cards: [Robber]\n"
        )
        verify_output_string(caplog, expected)

    @staticmethod
    def test_print_wolfbot_guesses(
        caplog: pytest.LogCaptureFixture, medium_game_roles: tuple[Role, ...]
    ) -> None:
        """Correctly print and format roles."""
        util.print_roles(medium_game_roles, "WolfBot")

        expected = (
            "[WolfBot] Player roles: [Robber, Drunk, Wolf, Troublemaker, Seer]\n"
            "          Center cards: [Minion]\n"
        )
        verify_output_string(caplog, expected)


class TestSwapCharacters:
    """Tests for the swap_characters function."""

    @staticmethod
    def test_same_index_error(small_game_roles: tuple[Role, ...]) -> None:
        """Don't attempt to swap the same index."""
        with pytest.raises(RuntimeError):
            util.swap_characters(list(small_game_roles), 2, 2)

    @staticmethod
    def test_swap(small_game_roles: tuple[Role, ...]) -> None:
        """Correctly swap two players."""
        roles = list(small_game_roles)

        util.swap_characters(roles, 0, 2)

        assert roles == [Role.ROBBER, Role.SEER, Role.VILLAGER]


class TestFindAllPlayerIndices:
    """Tests for the find_all_player_indices function."""

    @staticmethod
    def test_returns_correct_indices(large_game_roles: tuple[Role, ...]) -> None:
        """Don't attempt to swap the same index."""
        result = util.find_all_player_indices(large_game_roles, Role.VILLAGER)

        assert result == (1, 4, 11)
