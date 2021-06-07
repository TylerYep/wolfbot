""" one_night_test.py """
import pytest

from conftest import set_roles, verify_output, verify_output_string
from wolfbot import const, one_night
from wolfbot.const import Role, Team
from wolfbot.roles import Drunk, Minion, Player, Robber, Seer, Wolf
from wolfbot.statements import Statement


class TestGetIndividualPreds:
    """Tests for the get_individual_preds function."""

    @staticmethod
    def test_medium_individual_preds(
        medium_game_roles: tuple[Role, ...],
        medium_statement_list: tuple[Statement, ...],
    ) -> None:
        """Should get the individual predictions for all players."""
        player_objs: tuple[Player, ...] = (
            Seer(0, (2, Role.DRUNK)),
            Wolf(1, (1,), 5, Role.TROUBLEMAKER),
            Drunk(2, 5),
            Robber(3, 1, Role.WOLF),
            Minion(4, (1,)),
        )

        result = one_night.get_individual_preds(player_objs, medium_statement_list)

        assert result == (
            (
                Role.SEER,
                Role.MINION,
                Role.TROUBLEMAKER,
                Role.DRUNK,
                Role.WOLF,
                Role.ROBBER,
            ),
            (
                Role.MINION,
                Role.SEER,
                Role.TROUBLEMAKER,
                Role.WOLF,
                Role.ROBBER,
                Role.DRUNK,
            ),
            (
                Role.SEER,
                Role.MINION,
                Role.TROUBLEMAKER,
                Role.DRUNK,
                Role.WOLF,
                Role.ROBBER,
            ),
            (
                Role.SEER,
                Role.MINION,
                Role.TROUBLEMAKER,
                Role.DRUNK,
                Role.WOLF,
                Role.ROBBER,
            ),
            (
                Role.MINION,
                Role.WOLF,
                Role.TROUBLEMAKER,
                Role.DRUNK,
                Role.SEER,
                Role.ROBBER,
            ),
        )


class TestConfidence:
    """
    Tests for the get_confidence function.
    The order of the indiv_preds does not matter.
    """

    @staticmethod
    def test_small_confidence(small_game_roles: tuple[Role, ...]) -> None:
        """Should get voting results from the individual predictions."""
        indiv_preds = ((Role.VILLAGER, Role.SEER, Role.ROBBER),) * 3

        result = one_night.get_confidence(indiv_preds)

        assert result == (1,) * 3

    @staticmethod
    def test_medium_confidence(medium_game_roles: tuple[Role, ...]) -> None:
        """Should get voting results from the individual predictions."""
        indiv_preds = (
            (
                Role.SEER,
                Role.WOLF,
                Role.TROUBLEMAKER,
                Role.DRUNK,
                Role.MINION,
                Role.ROBBER,
            ),
            (
                Role.WOLF,
                Role.SEER,
                Role.ROBBER,
                Role.MINION,
                Role.TROUBLEMAKER,
                Role.DRUNK,
            ),
            (
                Role.SEER,
                Role.WOLF,
                Role.TROUBLEMAKER,
                Role.DRUNK,
                Role.MINION,
                Role.ROBBER,
            ),
            (
                Role.WOLF,
                Role.MINION,
                Role.TROUBLEMAKER,
                Role.DRUNK,
                Role.SEER,
                Role.ROBBER,
            ),
            (
                Role.WOLF,
                Role.MINION,
                Role.TROUBLEMAKER,
                Role.DRUNK,
                Role.SEER,
                Role.ROBBER,
            ),
        )

        result = one_night.get_confidence(indiv_preds)

        assert result == (0.6, 0.4, 0.8, 0.8, 0.4, 0.8)

    @staticmethod
    def test_large_confidence(
        large_game_roles: tuple[Role, ...],
        large_individual_preds: tuple[tuple[Role, ...], ...],
    ) -> None:
        """Should get voting results from the individual predictions."""
        result = one_night.get_confidence(large_individual_preds)

        assert result == (
            1,
            2 / 3,
            1,
            5 / 12,
            1,
            0.75,
            0.5,
            5 / 12,
            5 / 12,
            7 / 12,
            7 / 12,
            11 / 12,
            0.5,
            2 / 3,
            0.75,
        )


class TestGetVotingResult:
    """Tests for the get_voting_result function."""

    @staticmethod
    def test_small_voting_result(
        caplog: pytest.LogCaptureFixture, small_game_roles: tuple[Role, ...]
    ) -> None:
        """Should get voting results from the individual predictions."""
        indiv_preds = ((Role.VILLAGER, Role.SEER, Role.ROBBER),) * len(small_game_roles)
        player_list = tuple(Player(i) for i in range(len(small_game_roles)))

        result = one_night.get_voting_result(player_list, indiv_preds)

        assert result == ((Role.VILLAGER, Role.SEER, Role.ROBBER), (0, 1, 2), (1, 2, 0))
        verify_output_string(caplog, "\nVote Array: [1, 1, 1]\n")

    @staticmethod
    def test_medium_voting_result(
        caplog: pytest.LogCaptureFixture, medium_game_roles: tuple[Role, ...]
    ) -> None:
        """Should get voting results from the individual predictions."""
        indiv_preds = (
            (
                Role.SEER,
                Role.WOLF,
                Role.TROUBLEMAKER,
                Role.DRUNK,
                Role.MINION,
                Role.ROBBER,
            ),
            (
                Role.WOLF,
                Role.SEER,
                Role.ROBBER,
                Role.MINION,
                Role.TROUBLEMAKER,
                Role.DRUNK,
            ),
            (
                Role.SEER,
                Role.WOLF,
                Role.TROUBLEMAKER,
                Role.DRUNK,
                Role.MINION,
                Role.ROBBER,
            ),
            (
                Role.WOLF,
                Role.MINION,
                Role.TROUBLEMAKER,
                Role.DRUNK,
                Role.SEER,
                Role.ROBBER,
            ),
            (
                Role.WOLF,
                Role.MINION,
                Role.TROUBLEMAKER,
                Role.DRUNK,
                Role.SEER,
                Role.ROBBER,
            ),
        )
        player_list = tuple(Player(i) for i in range(len(medium_game_roles)))

        result = one_night.get_voting_result(player_list, indiv_preds)

        assert result == (
            (
                Role.SEER,
                Role.WOLF,
                Role.TROUBLEMAKER,
                Role.DRUNK,
                Role.MINION,
                Role.ROBBER,
            ),
            (0,),
            (1, 0, 1, 0, 0),
        )
        verify_output_string(caplog, "\nVote Array: [3, 2, 0, 0, 0]\n")

    @staticmethod
    def test_large_voting_result(
        caplog: pytest.LogCaptureFixture,
        large_game_roles: tuple[Role, ...],
        large_individual_preds: tuple[tuple[Role, ...], ...],
    ) -> None:
        """Should get voting results from the individual predictions."""
        player_list = tuple(Player(i) for i in range(len(large_game_roles)))

        result = one_night.get_voting_result(player_list, large_individual_preds)

        assert result == (
            (
                Role.VILLAGER,
                Role.MASON,
                Role.MASON,
                Role.MINION,
                Role.VILLAGER,
                Role.DRUNK,
                Role.TANNER,
                Role.TROUBLEMAKER,
                Role.VILLAGER,
                Role.WOLF,
                Role.WOLF,
                Role.HUNTER,
                Role.INSOMNIAC,
                Role.SEER,
                Role.ROBBER,
            ),
            (10,),
            (10, 10, 7, 5, 7, 10, 7, 10, 6, 10, 3, 10),
        )
        verify_output_string(
            caplog, "\nVote Array: [0, 0, 0, 1, 0, 1, 1, 3, 0, 0, 6, 0]\n"
        )


class TestEvalWinningTeam:
    """Tests for the eval_winning_team function."""

    @staticmethod
    def test_werewolf_wins(
        caplog: pytest.LogCaptureFixture, medium_game_roles: tuple[Role, ...]
    ) -> None:
        """Should declare Werewolf victory if no wolves are found, but one exists."""
        guessed_wolf_inds = list(range(const.NUM_PLAYERS))
        vote_inds = (1,) * const.NUM_PLAYERS

        result = one_night.eval_winning_team(
            medium_game_roles, guessed_wolf_inds, vote_inds
        )

        expected = (
            "No wolves were found.",
            "But Player(s) [2] was a Wolf!\n",
            "Werewolf Team wins!",
        )
        assert result is Team.WEREWOLF
        verify_output(caplog, expected)

    @staticmethod
    def test_village_wins_no_wolf(
        caplog: pytest.LogCaptureFixture, small_game_roles: tuple[Role, ...]
    ) -> None:
        """
        Should declare Villager victory if no wolves are found, and there are none.
        """
        guessed_wolf_inds = list(range(const.NUM_PLAYERS))
        vote_inds = (1,) * const.NUM_PLAYERS

        result = one_night.eval_winning_team(
            small_game_roles, guessed_wolf_inds, vote_inds
        )

        expected = (
            "No wolves were found.",
            "That was correct!\n",
            "Village Team wins!",
        )
        assert result is Team.VILLAGE
        verify_output(caplog, expected)

    @staticmethod
    def test_village_wins_found_wolf(
        caplog: pytest.LogCaptureFixture, medium_game_roles: tuple[Role, ...]
    ) -> None:
        """
        Should declare Villager victory if no wolves are found, and there are none.
        """
        guessed_wolf_inds = [2]
        vote_inds = (1, 2, 2, 2, 1)

        result = one_night.eval_winning_team(
            medium_game_roles, guessed_wolf_inds, vote_inds
        )

        expected = (
            "Player 2 was chosen as a Wolf.",
            "Player 2 was a Wolf!\n",
            "Village Team wins!",
        )
        assert result is Team.VILLAGE
        verify_output(caplog, expected)

    @staticmethod
    def test_hunter_wins(
        caplog: pytest.LogCaptureFixture, large_game_roles: tuple[Role, ...]
    ) -> None:
        """
        Should declare Village victory if no wolves are found,
        Hunter is killed, and Hunter voted for a true Wolf.
        """
        set_roles(*large_game_roles[::-1])
        guessed_wolf_inds = [0, 9]
        vote_inds = (7, 10, 0, 9, 7, 9, 7, 7, 7, 0, 0, 0)
        expected = (
            "Player 0 was chosen as a Wolf.",
            "Player 0 was a Hunter!\n",
            "(Player 0) Hunter died and killed Player 7 too!\n",
            "Player 9 was chosen as a Wolf.",
            "Player 9 was a Tanner!\n",
            "Player 7 was chosen as a Wolf.",
            "Player 7 was a Wolf!\n",
            "Village Team wins!",
        )

        result = one_night.eval_winning_team(const.ROLES, guessed_wolf_inds, vote_inds)

        assert result is Team.VILLAGE
        verify_output(caplog, expected)

    @staticmethod
    def test_tanner_wins(
        caplog: pytest.LogCaptureFixture, large_game_roles: tuple[Role, ...]
    ) -> None:
        """
        Should declare Tanner victory if no wolves are found, and Tanner was chosen.
        """
        guessed_wolf_inds = [2, 5]
        vote_inds = (8, 7, 1, 9, 5, 10, 5, 3, 3, 10, 10, 3)

        result = one_night.eval_winning_team(
            large_game_roles, guessed_wolf_inds, vote_inds
        )

        expected = (
            "Player 2 was chosen as a Wolf.",
            "Player 2 was a Robber!\n",
            "Player 5 was chosen as a Wolf.",
            "Player 5 was a Tanner!\n",
            "Tanner wins!",
        )
        assert result is Team.TANNER
        verify_output(caplog, expected)
