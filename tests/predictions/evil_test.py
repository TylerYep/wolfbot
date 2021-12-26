from wolfbot import predictions
from wolfbot.enums import Role
from wolfbot.solvers import SolverState


class TestMakeRandomPrediction:
    """Tests for the random_prediction function."""

    @staticmethod
    def test_random_prediction(medium_game_roles: tuple[Role, ...]) -> None:
        """Should return a random shuffled list as the predicted roles."""
        result = predictions.make_random_prediction()

        assert result == (
            Role.SEER,
            Role.WOLF,
            Role.DRUNK,
            Role.ROBBER,
            Role.MINION,
            Role.TROUBLEMAKER,
        )


class TestMakeEvilPrediction:
    """Tests for the make_evil_prediction function."""

    @staticmethod
    def test_random_evil_prediction(medium_game_roles: tuple[Role, ...]) -> None:
        """Should give a random prediction when an empty SolverState is passed in."""
        solution_arr = ()

        result = predictions.make_evil_prediction(solution_arr)

        assert result == (
            Role.SEER,
            Role.WOLF,
            Role.DRUNK,
            Role.ROBBER,
            Role.MINION,
            Role.TROUBLEMAKER,
        )

    @staticmethod
    def test_evil_prediction(
        example_medium_solverstate_list: tuple[SolverState, ...]
    ) -> None:
        """Should give a random prediction when an empty SolverState is passed in."""
        result = predictions.make_evil_prediction(example_medium_solverstate_list)

        assert result == (
            Role.SEER,
            Role.MINION,
            Role.TROUBLEMAKER,
            Role.DRUNK,
            Role.WOLF,
            Role.ROBBER,
        )


class TestMakeUnrestrictedPrediction:
    """Tests for the make_unrestricted_prediction function."""

    @staticmethod
    def test_empty_unrestricted_prediction(medium_game_roles: tuple[Role, ...]) -> None:
        """Should return an empty list to denote that no prediction could be made."""
        solution = SolverState()

        result = predictions.make_unrestricted_prediction(solution)

        assert result == (
            Role.TROUBLEMAKER,
            Role.DRUNK,
            Role.WOLF,
            Role.SEER,
            Role.ROBBER,
            Role.MINION,
        )

    @staticmethod
    def test_unrestricted_prediction(example_medium_solverstate: SolverState) -> None:
        """
        Should return a list of predictions without
        requiring adherence to possible sets.
        """
        result = predictions.make_unrestricted_prediction(example_medium_solverstate)

        assert result == (
            Role.SEER,
            Role.TROUBLEMAKER,
            Role.WOLF,
            Role.MINION,
            Role.ROBBER,
            Role.DRUNK,
        )
