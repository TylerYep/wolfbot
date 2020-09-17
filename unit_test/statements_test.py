""" statements_test.py """
from typing import Tuple

from src import const, statements
from src.const import Role, StatementLevel, SwitchPriority
from src.statements import KnowledgeBase, Statement


class TestKnowledgeBase:
    """ Tests for the KnowledgeBase class. """

    @staticmethod
    def test_add_knowledge(example_statement: Statement) -> None:
        """ Should initialize using the given sentence and knowledge. """
        knowledge_base = KnowledgeBase()
        next_statement = Statement("test", ((1, frozenset({Role.VILLAGER})),))

        knowledge_base.add(example_statement, 0)
        knowledge_base.add(next_statement, 1)

        not_yet_spoken = statements.Statement(
            "", priority=StatementLevel.NOT_YET_SPOKEN
        )
        assert knowledge_base.all_statements == [example_statement, next_statement]
        assert knowledge_base.stated_roles == [Role.ROBBER, Role.VILLAGER] + (
            [Role.NONE] * 10
        )
        assert knowledge_base.final_claims == (
            [example_statement, next_statement] + ([not_yet_spoken] * 10)
        )


class TestStatement:
    """ Tests for the Statement class. """

    @staticmethod
    def test_constructor() -> None:
        """ Should initialize using the given sentence and knowledge. """
        result = Statement("test", ((1, frozenset({Role.VILLAGER})),))

        assert result.sentence == "test"
        assert result.knowledge == ((1, frozenset({Role.VILLAGER})),)
        assert result.switches == ()
        assert result.speaker is Role.VILLAGER

    @staticmethod
    def test_references_true(example_statement: Statement) -> None:
        """ Should return True if a given player_index is referenced in a statement. """
        result = example_statement.references(0)

        assert result is True

    @staticmethod
    def test_references_false(example_statement: Statement) -> None:
        """ Should return True if a given player_index is referenced in a statement. """
        result = example_statement.references(1)

        assert result is False

    @staticmethod
    def test_negation(
        large_game_roles: Tuple[Role, ...], example_statement: Statement
    ) -> None:
        """
        Negated statements only contain the speaker and
        the opposite of the first clause.
        """
        expected = Statement(
            "NOT - test",
            ((2, const.ROLE_SET - frozenset({Role.ROBBER})),),
            speaker=Role.ROBBER,
        )

        result = example_statement.negation

        assert str(result) == str(expected)

    @staticmethod
    def test_negate_all(
        large_game_roles: Tuple[Role, ...], example_statement: Statement
    ) -> None:
        """ Negate-all statements contain the opposite of all clauses. """
        expected = Statement(
            "NOT - test",
            (
                (2, const.ROLE_SET - frozenset({Role.ROBBER})),
                (0, const.ROLE_SET - frozenset({Role.SEER})),
            ),
            speaker=Role.ROBBER,
        )

        result = example_statement.negate_all()

        assert str(result) == str(expected)

    @staticmethod
    def test_json_repr(example_statement: Statement) -> None:
        """ Should convert a Statement into a dict with all of its fields. """
        result = example_statement.json_repr()

        assert result == {
            "type": "Statement",
            "sentence": "test",
            "knowledge": ((2, frozenset({Role.ROBBER})), (0, frozenset({Role.SEER}))),
            "switches": ((SwitchPriority.ROBBER, 2, 0),),
            "speaker": Role.ROBBER,
        }

    @staticmethod
    def test_eq(example_statement: Statement) -> None:
        """ Should declare two Statements with identical fields to be equal. """
        result = Statement(
            "test",
            ((2, frozenset({Role.ROBBER})), (0, frozenset({Role.SEER}))),
            ((SwitchPriority.ROBBER, 2, 0),),
        )

        assert result == example_statement

    @staticmethod
    def test_hash(example_statement: Statement) -> None:
        """ Should give two Statements with identical fields the same hash. """
        identical_statement = Statement(
            "test",
            ((2, frozenset({Role.ROBBER})), (0, frozenset({Role.SEER}))),
            ((SwitchPriority.ROBBER, 2, 0),),
        )

        result = {identical_statement, example_statement}

        assert result == {example_statement}
