from tests.conftest import set_roles
from wolfbot import const
from wolfbot.enums import Role, SwitchPriority
from wolfbot.solvers import SolverState
from wolfbot.statements import Statement


class TestSolverState:
    """Tests for the SolverState class."""

    @staticmethod
    def test_constructor() -> None:
        """Should initialize a SolverState."""
        result = SolverState((frozenset({Role.VILLAGER}),), path=(True,))

        assert isinstance(result, SolverState)

    @staticmethod
    def test_eq(example_small_solverstate: SolverState) -> None:
        """Should be able to compare two identical SolverStates."""
        possible_roles = (
            frozenset({Role.SEER}),
            frozenset({Role.ROBBER, Role.VILLAGER, Role.SEER}),
            frozenset({Role.ROBBER}),
        )
        switches = ((SwitchPriority.ROBBER, 2, 0),)
        path = (True,)

        result = SolverState(possible_roles, switches, path)

        assert result == example_small_solverstate

    @staticmethod
    def test_get_role_counts() -> None:
        """
        Should return True if there is a a dict with counts of all certain roles.
        """
        set_roles(Role.WOLF, Role.SEER, Role.VILLAGER, Role.ROBBER, Role.VILLAGER)
        possible_roles_list = (
            frozenset({Role.VILLAGER}),
            frozenset({Role.SEER}),
            frozenset({Role.VILLAGER}),
        ) + (const.ROLE_SET,) * 2

        result = SolverState(possible_roles_list).get_role_counts()

        assert result == {Role.SEER: 0, Role.VILLAGER: 0, Role.WOLF: 1, Role.ROBBER: 1}

    @staticmethod
    def test_repr() -> None:
        """Should pretty-print SolverStates using the custom formatter."""
        result = SolverState((frozenset({Role.VILLAGER}),), path=(True,))

        assert (
            str(result)
            == repr(result)
            == (
                "SolverState(\n"
                "    possible_roles=(frozenset([Role.VILLAGER]),),\n"
                "    path=(True,),\n"
                "    role_counts={\n"
                "        Role.INSOMNIAC: 1,\n"
                "        Role.VILLAGER: 2,\n"
                "        Role.ROBBER: 1,\n"
                "        Role.DRUNK: 1,\n"
                "        Role.WOLF: 2,\n"
                "        Role.SEER: 1,\n"
                "        Role.TANNER: 1,\n"
                "        Role.MASON: 2,\n"
                "        Role.MINION: 1,\n"
                "        Role.TROUBLEMAKER: 1,\n"
                "        Role.HUNTER: 1\n"
                "    },\n"
                "    count_true=1\n"
                ")"
            )
        )


class TestIsConsistent:
    """Tests for the is_consistent function."""

    @staticmethod
    def test_is_consistent_on_empty_state(
        example_small_solverstate: SolverState, example_statement: Statement
    ) -> None:
        """
        Should check a new statement against an empty SolverState for consistency.
        """
        start_state = SolverState()

        result = start_state.is_consistent(example_statement)

        assert result == example_small_solverstate

    @staticmethod
    def test_invalid_state(example_statement: Statement) -> None:
        """Should return None for inconsistent states."""
        start_state = SolverState((frozenset({Role.VILLAGER}),) * 3, path=(True,))

        invalid_state = start_state.is_consistent(example_statement)

        assert invalid_state is None

    @staticmethod
    def test_is_consistent_on_existing_state(
        example_medium_solverstate: SolverState,
    ) -> None:
        """
        Should check a new statement against accumulated statements for consistency.
        Should not change result.path - that is done in the switching_solver function.
        """
        possible_roles = (frozenset({Role.SEER}),) + (const.ROLE_SET,) * (
            const.NUM_ROLES - 1
        )
        example_solverstate = SolverState(possible_roles, path=(True,))
        new_statement = Statement(
            "next", ((2, frozenset({Role.DRUNK})),), ((SwitchPriority.DRUNK, 2, 5),)
        )

        result = example_solverstate.is_consistent(new_statement)

        assert result == example_medium_solverstate

    @staticmethod
    def test_is_consistent_deepcopy_mechanics(
        example_medium_solverstate: SolverState,
    ) -> None:
        """
        Modifying one SolverState should not affect
        other SolverStates created by is_consistent.
        """
        possible_roles = (frozenset({Role.SEER}),) + (const.ROLE_SET,) * (
            const.NUM_ROLES - 1
        )
        example = SolverState(possible_roles, path=(True,))
        new_statement = Statement(
            "next", ((2, frozenset({Role.DRUNK})),), ((SwitchPriority.DRUNK, 2, 5),)
        )

        result = example.is_consistent(new_statement)
        example.possible_roles += (frozenset({Role.NONE}),)
        example.switches += ((SwitchPriority.DRUNK, 5, 5),)
        example.possible_roles = (example.possible_roles[0] & {Role.NONE},)

        assert result == example_medium_solverstate
