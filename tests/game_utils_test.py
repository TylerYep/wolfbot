import pytest

from tests.conftest import override_input, verify_output_string
from wolfbot.enums import Role
from wolfbot.game_utils import (
    find_all_player_indices,
    get_center,
    get_numeric_input,
    get_player,
    print_roles,
    swap_characters,
)


class TestPrintRoles:
    """Tests for the print_roles function."""

    @staticmethod
    def test_print_roles(
        caplog: pytest.LogCaptureFixture, small_game_roles: tuple[Role, ...]
    ) -> None:
        """Correctly print and format roles."""
        shuffled_roles = [Role.SEER, Role.VILLAGER, Role.WOLF, Role.ROBBER]

        print_roles(shuffled_roles, "Hidden")

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
        print_roles(medium_game_roles, "WolfBot")

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
            swap_characters(list(small_game_roles), 2, 2)

    @staticmethod
    def test_swap(small_game_roles: tuple[Role, ...]) -> None:
        """Correctly swap two players."""
        roles = list(small_game_roles)

        swap_characters(roles, 0, 2)

        assert roles == [Role.ROBBER, Role.SEER, Role.VILLAGER]


class TestFindAllPlayerIndices:
    """Tests for the find_all_player_indices function."""

    @staticmethod
    def test_returns_correct_indices(large_game_roles: tuple[Role, ...]) -> None:
        """Don't attempt to swap the same index."""
        result = find_all_player_indices(large_game_roles, Role.VILLAGER)

        assert result == (1, 4, 11)


class TestGetPlayer:
    """Tests for the get_player function."""

    @staticmethod
    def test_generates_random_indices(large_game_roles: tuple[Role, ...]) -> None:
        """Generated indices should be random."""
        result = [get_player(is_user=False) for _ in range(10)]

        assert result == [6, 6, 0, 4, 8, 7, 6, 4, 7, 5]

    @staticmethod
    def test_random_excludes_values(large_game_roles: tuple[Role, ...]) -> None:
        """Generated indices should exclude specified values."""
        exclude = (6, 7, 8)

        result = [get_player(is_user=False, exclude=exclude) for _ in range(10)]

        assert not set(result).intersection(exclude)
        assert result == [9, 9, 0, 4, 11, 10, 9, 4, 10, 5]

    @staticmethod
    def test_user_input_indices(
        monkeypatch: pytest.MonkeyPatch, large_game_roles: tuple[Role, ...]
    ) -> None:
        """Generated indices should be random."""
        inputs = [0, 2, 20, 1]
        monkeypatch.setattr("builtins.input", override_input([str(i) for i in inputs]))

        result = [get_player(is_user=True) for _ in range(3)]

        assert result == [0, 2, 1]

    @staticmethod
    def test_user_excludes_values(
        monkeypatch: pytest.MonkeyPatch, large_game_roles: tuple[Role, ...]
    ) -> None:
        """Generated indices should exclude specified values."""
        exclude = (6, 7, 8)
        inputs = [0, 20, 4, 7, 5, 6]
        monkeypatch.setattr("builtins.input", override_input([str(i) for i in inputs]))

        result = [get_player(is_user=True, exclude=exclude) for _ in range(3)]

        assert not set(result).intersection(exclude)
        assert result == [0, 4, 5]


class TestGetCenter:
    """Tests for the get_center function."""

    @staticmethod
    def test_generates_random_indices(large_game_roles: tuple[Role, ...]) -> None:
        """Generated indices should be random."""
        result = [get_center(is_user=False) for _ in range(10)]

        assert result == [13, 13, 12, 13, 14, 13, 13, 13, 13, 13]

    @staticmethod
    def test_excludes_values(large_game_roles: tuple[str, ...]) -> None:
        """Generated indices should exclude specified values."""
        exclude = (12, 13)

        result = [get_center(is_user=False, exclude=exclude) for _ in range(10)]

        assert not set(result).intersection(exclude)
        assert result == [14] * 10

    @staticmethod
    def test_user_center_indices(
        monkeypatch: pytest.MonkeyPatch, large_game_roles: tuple[Role, ...]
    ) -> None:
        """Generated indices should be random."""
        inputs = [1, 2, 0, 2]
        monkeypatch.setattr("builtins.input", override_input([str(i) for i in inputs]))

        result = [get_center(is_user=True) for _ in range(3)]

        assert result == [13, 14, 12]

    @staticmethod
    def test_user_excludes_values(
        monkeypatch: pytest.MonkeyPatch, large_game_roles: tuple[Role, ...]
    ) -> None:
        """Generated indices should exclude specified values."""
        exclude = (12, 13)
        inputs = [2, 0, 4, 1, 2, 2]
        monkeypatch.setattr("builtins.input", override_input([str(i) for i in inputs]))

        result = [get_center(is_user=True, exclude=exclude) for _ in range(3)]

        assert not set(result).intersection(exclude)
        assert result == [14] * 3


class TestGetNumericInput:
    """Tests for the get_numeric_input function."""

    @staticmethod
    def test_numeric_input(monkeypatch: pytest.MonkeyPatch) -> None:
        """Generated indices should be random."""
        inputs = [1, 7, 10, 15, 2, 0]
        monkeypatch.setattr("builtins.input", override_input([str(i) for i in inputs]))

        result = [get_numeric_input(10) for _ in range(4)]

        assert result == [1, 7, 2, 0]

    @staticmethod
    def test_numeric_input_range(monkeypatch: pytest.MonkeyPatch) -> None:
        """Generated indices should be random."""
        inputs = [1, 37, 30, 34, 0, 33]
        monkeypatch.setattr("builtins.input", override_input([str(i) for i in inputs]))

        result = [get_numeric_input(30, 34) for _ in range(2)]

        assert result == [30, 33]
