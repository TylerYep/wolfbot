""" statements_test.py """
from src import const, statements
from src.const import SwitchPriority


class TestStatement:
    """ Tests for the Statement class. """

    @staticmethod
    def test_constructor():
        """ Should initialize using the given sentence and knowledge. """
        result = statements.Statement("test", ((1, frozenset({"Villager"})),))

        assert isinstance(result, statements.Statement)
        assert result.sentence == "test"
        assert result.knowledge == ((1, frozenset({"Villager"})),)
        assert result.switches == ()
        assert result.speaker == "Villager"

    @staticmethod
    def test_references_true(example_statement):
        """ Should return True if a given player_index is referenced in a statement. """
        result = example_statement.references(0)

        assert result is True

    @staticmethod
    def test_references_false(example_statement):
        """ Should return True if a given player_index is referenced in a statement. """
        result = example_statement.references(1)

        assert result is False

    @staticmethod
    def test_negation(large_game_roles, example_statement):
        """ Negated statements only contain the speaker and the opposite of the first clause. """
        expected = statements.Statement(
            "NOT - test", ((2, const.ROLE_SET - frozenset({"Robber"})),), speaker="Robber"
        )

        result = example_statement.negation

        assert isinstance(result, statements.Statement)
        assert str(result) == str(expected)

    @staticmethod
    def test_negate_all(large_game_roles, example_statement):
        """ Negate-all statements contain the opposite of all clauses. """
        expected = statements.Statement(
            "NOT - test",
            (
                (2, const.ROLE_SET - frozenset({"Robber"})),
                (0, const.ROLE_SET - frozenset({"Seer"})),
            ),
            speaker="Robber",
        )

        result = example_statement.negate_all()

        assert isinstance(result, statements.Statement)
        assert str(result) == str(expected)

    @staticmethod
    def test_json_repr(example_statement):
        """ Should convert a Statement into a dict with all of its fields. """
        result = example_statement.json_repr()

        assert result == {
            "type": "Statement",
            "sentence": "test",
            "knowledge": ((2, frozenset({"Robber"})), (0, frozenset({"Seer"}))),
            "switches": ((SwitchPriority.ROBBER, 2, 0),),
            "speaker": "Robber",
        }

    @staticmethod
    def test_repr(example_statement):
        """ Should convert a Statement into a string with all useful fields. """
        expected = (
            "Statement(sentence='test', knowledge=((2, frozenset({'Robber'})), (0, "
            "frozenset({'Seer'}))), switches=((<SwitchPriority.ROBBER: 1>, 2, 0),), "
            "speaker='Robber', priority=<StatementLevel.PRIMARY: 10>)"
        )

        result = str(example_statement)

        assert result == expected

    @staticmethod
    def test_eq(example_statement):
        """ Should declare two Statements with identical fields to be equal. """
        result = statements.Statement(
            "test",
            ((2, frozenset({"Robber"})), (0, frozenset({"Seer"})),),
            ((SwitchPriority.ROBBER, 2, 0),),
        )

        assert result == example_statement

    @staticmethod
    def test_hash(example_statement):
        """ Should give two Statements with identical fields the same hash. """
        identical_statement = statements.Statement(
            "test",
            ((2, frozenset({"Robber"})), (0, frozenset({"Seer"})),),
            ((SwitchPriority.ROBBER, 2, 0),),
        )

        result = {identical_statement, example_statement}

        assert result == {example_statement}
