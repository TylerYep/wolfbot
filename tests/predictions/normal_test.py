from wolfbot import predictions
from wolfbot.enums import Role
from wolfbot.solvers import SolverState


class TestMakePrediction:
    """Tests for the make_prediction function."""

    @staticmethod
    def test_make_evil_prediction(
        example_medium_solverstate_list: tuple[SolverState, ...],
    ) -> None:
        """Should return evil prediction when is_evil=True."""
        result = predictions.make_prediction(
            example_medium_solverstate_list, is_evil=True
        )

        assert result == (
            Role.SEER,
            Role.MINION,
            Role.TROUBLEMAKER,
            Role.DRUNK,
            Role.WOLF,
            Role.ROBBER,
        )

    @staticmethod
    def test_make_prediction(
        example_medium_solverstate_list: tuple[SolverState, ...],
    ) -> None:
        """Should return valid prediction for villager players."""
        result = predictions.make_prediction(
            example_medium_solverstate_list, is_evil=False
        )

        assert result == (
            Role.ROBBER,
            Role.SEER,
            Role.TROUBLEMAKER,
            Role.WOLF,
            Role.MINION,
            Role.DRUNK,
        )
