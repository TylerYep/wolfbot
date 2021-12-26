from wolfbot import const, predictions
from wolfbot.const import Role
from wolfbot.solvers import SolverState


class TestGetBasicGuesses:
    """Tests for the get_basic_guesses function."""

    @staticmethod
    def test_guesses_small(example_small_solverstate: SolverState) -> None:
        """
        Should correctly interpret a solution as a list of current predictions
        as well as a dictionary of counts.
        """
        result = predictions.get_basic_guesses(example_small_solverstate)

        assert result == (
            [Role.SEER, Role.NONE, Role.ROBBER],
            {Role.ROBBER: 0, Role.SEER: 0, Role.VILLAGER: 1},
        )

    @staticmethod
    def test_guesses_medium(example_medium_solverstate: SolverState) -> None:
        """
        Should correctly interpret a solution as a list of current predictions
        as well as a dictionary of counts.
        """
        result = predictions.get_basic_guesses(example_medium_solverstate)

        assert result == (
            [Role.SEER, Role.NONE, Role.DRUNK, Role.NONE, Role.NONE, Role.NONE],
            {
                Role.DRUNK: 0,
                Role.MINION: 1,
                Role.ROBBER: 1,
                Role.SEER: 0,
                Role.TROUBLEMAKER: 1,
                Role.WOLF: 1,
            },
        )

    @staticmethod
    def test_guesses_large(example_large_solverstate: SolverState) -> None:
        """
        Should correctly interpret a solution as a list of current predictions
        as well as a dictionary of counts.
        """
        result = predictions.get_basic_guesses(example_large_solverstate)

        assert result == (
            [
                Role.ROBBER,
                Role.MINION,
                Role.SEER,
                Role.VILLAGER,
                Role.MASON,
                Role.MASON,
                Role.DRUNK,
                Role.WOLF,
            ]
            + [Role.NONE] * 7,
            {
                Role.DRUNK: 0,
                Role.HUNTER: 1,
                Role.INSOMNIAC: 1,
                Role.MASON: 0,
                Role.MINION: 0,
                Role.ROBBER: 0,
                Role.SEER: 0,
                Role.TANNER: 1,
                Role.TROUBLEMAKER: 1,
                Role.VILLAGER: 2,
                Role.WOLF: 1,
            },
        )


class TestRecurseAssign:
    """Tests for the recurse_assign function."""

    @staticmethod
    def test_no_action(
        example_small_solverstate: SolverState, small_game_roles: tuple[Role, ...]
    ) -> None:
        """Should not make any assignments if all assignments are made."""
        counts = {Role.ROBBER: 0, Role.SEER: 0, Role.VILLAGER: 0}

        result = predictions.recurse_assign(
            example_small_solverstate, list(small_game_roles), counts
        )

        assert result == list(small_game_roles)

    @staticmethod
    def test_no_solution_medium(example_medium_solverstate: SolverState) -> None:
        """Should return empty list if no arrangement of assignments is valid."""
        role_guesses = [
            Role.ROBBER,
            Role.NONE,
            Role.SEER,
            Role.VILLAGER,
            Role.MASON,
            Role.MASON,
            Role.DRUNK,
        ] + [Role.NONE] * 8
        counts = {
            Role.DRUNK: 0,
            Role.HUNTER: 1,
            Role.INSOMNIAC: 1,
            Role.MASON: 0,
            Role.MINION: 1,
            Role.ROBBER: 0,
            Role.SEER: 0,
            Role.TANNER: 1,
            Role.TROUBLEMAKER: 1,
            Role.VILLAGER: 2,
            Role.WOLF: 2,
        }

        result = predictions.recurse_assign(
            example_medium_solverstate, role_guesses, counts
        )

        assert result == []

    @staticmethod
    def test_small_predict_solution(example_small_solverstate: SolverState) -> None:
        """
        Should return solved list if there is an arrangement of valid assignments.
        """
        role_guesses = [Role.SEER, Role.NONE, Role.ROBBER]
        counts = {Role.ROBBER: 0, Role.SEER: 0, Role.VILLAGER: 1}

        result = predictions.recurse_assign(
            example_small_solverstate, role_guesses, counts
        )

        assert result == [Role.SEER, Role.VILLAGER, Role.ROBBER]

    @staticmethod
    def test_medium_predict_solution(example_medium_solverstate: SolverState) -> None:
        """
        Should return solved list if there is an arrangement of valid assignments.
        """
        role_guesses = [
            Role.SEER,
            Role.NONE,
            Role.DRUNK,
            Role.NONE,
            Role.NONE,
            Role.NONE,
        ]
        counts = {
            Role.DRUNK: 0,
            Role.MINION: 1,
            Role.ROBBER: 1,
            Role.SEER: 0,
            Role.TROUBLEMAKER: 1,
            Role.WOLF: 1,
        }

        result = predictions.recurse_assign(
            example_medium_solverstate, role_guesses, counts
        )

        assert result == [
            Role.SEER,
            Role.TROUBLEMAKER,
            Role.DRUNK,
            Role.MINION,
            Role.WOLF,
            Role.ROBBER,
        ]

    @staticmethod
    def test_large_predict_solution(example_large_solverstate: SolverState) -> None:
        """
        Should return solved list if there is an arrangement of valid assignments.
        """
        role_guesses = [
            Role.ROBBER,
            Role.NONE,
            Role.SEER,
            Role.VILLAGER,
            Role.MASON,
            Role.MASON,
            Role.DRUNK,
        ] + [Role.NONE] * 8
        counts = {
            Role.DRUNK: 0,
            Role.HUNTER: 1,
            Role.INSOMNIAC: 1,
            Role.MASON: 0,
            Role.MINION: 1,
            Role.ROBBER: 0,
            Role.SEER: 0,
            Role.TANNER: 1,
            Role.TROUBLEMAKER: 1,
            Role.VILLAGER: 2,
            Role.WOLF: 2,
        }

        result = predictions.recurse_assign(
            example_large_solverstate, role_guesses, counts
        )

        assert result == [
            Role.ROBBER,
            Role.TROUBLEMAKER,
            Role.SEER,
            Role.VILLAGER,
            Role.MASON,
            Role.MASON,
            Role.DRUNK,
            Role.WOLF,
            Role.TANNER,
            Role.HUNTER,
            Role.MINION,
            Role.INSOMNIAC,
            Role.VILLAGER,
            Role.VILLAGER,
            Role.WOLF,
        ]


class TestGetSwitchDict:
    """Tests for the get_switch_dict function."""

    @staticmethod
    def test_get_empty_switch_dict(small_game_roles: tuple[Role, ...]) -> None:
        """Should return the identity switch dict."""
        possible_roles = (frozenset({Role.ROBBER, Role.VILLAGER, Role.SEER}),) * 3
        state = SolverState(possible_roles)

        result = predictions.get_switch_dict(state)

        assert result == {i: i for i in range(const.NUM_ROLES)}

    @staticmethod
    def test_get_switch_dict(example_large_solverstate: SolverState) -> None:
        """Should return the correct switch dict for a SolverState result."""
        expected = {i: i for i in range(const.NUM_ROLES)}
        expected[6] = 9
        expected[0] = 6
        expected[9] = 0

        result = predictions.get_switch_dict(example_large_solverstate)

        assert result == expected
