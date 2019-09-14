''' algorithms_test.py '''
from src import algorithms, const
from src.statements import Statement

STATEMENT_LIST = [
    Statement('I am a Robber and I swapped with Player 6. I am now a Drunk.',
              [(0, {'Robber'}), (6, {'Drunk'})], [(0, 6, 0)]),
    Statement('I am a Robber and I swapped with Player 0. I am now a Seer.',
              [(1, {'Robber'}), (0, {'Seer'})], [(0, 0, 1)]),
    Statement('I am a Seer and I saw that Player 3 was a Villager.',
              [(2, {'Seer'}), (3, {'Villager'})], []),
    Statement('I am a Villager.', [(3, {'Villager'})], []),
    Statement('I am a Mason. The other Mason is Player 5.',
              [(4, {'Mason'}), (5, {'Mason'})], []),
    Statement('I am a Mason. The other Mason is Player 4.',
              [(5, {'Mason'}), (4, {'Mason'})], []),
    Statement('I am a Drunk and I swapped with Center 1.',
              [(6, {'Drunk'})], [(1, 9, 6)]),
    Statement('I am a Robber and I swapped with Player 5. I am now a Seer.',
              [(7, {'Robber'}), (5, {'Seer'})], [(0, 5, 7)])
]

POSSIBLE_ROLES = [

]

SWITCHES = [

]

PATH = [True, False, True, True, True, True, True, False]

class TestSolverState:
    def test_constructor(self):
        state = algorithms.SolverState([{'Villager'}])

        assert isinstance(state, algorithms.SolverState)

    def test_is_valid_state(self):
        valid_state = algorithms.SolverState([{'Villager'}])
        invalid_state = algorithms.SolverState([])

        assert valid_state.is_valid_state()
        assert not invalid_state.is_valid_state()

    def test_repr(self):
        state = algorithms.SolverState([{'Villager'}])

        assert str(state) == "\n[{'Villager'}]\n[]\n[]\n" # TODO


class TestIsConsistent:
    pass


class TestSolver:
    def test_switching_solver(self):
        expected_possible_roles = [
            {'Robber'},
            {'Seer', 'Hunter', 'Drunk', 'Tanner', 'Wolf', 'Insomniac',
             'Mason', 'Minion', 'Villager', 'Troublemaker'},
            {'Seer'},
            {'Villager'},
            {'Mason'},
            {'Mason'},
            {'Drunk'},
            {'Seer', 'Hunter', 'Drunk', 'Tanner', 'Wolf', 'Insomniac', 'Mason',
             'Minion', 'Villager', 'Troublemaker'}
        ] + [const.ROLE_SET]*7
        expected_path = [True, False, True, True, True, True, True, False]

        result = algorithms.switching_solver(STATEMENT_LIST)

        assert result[0].possible_roles == expected_possible_roles
        assert result[0].path == expected_path

    def test_count_roles(self):
        const.ROLE_SET = set(['Wolf', 'Seer', 'Villager'])
        possible_roles_list = [
            {'Villager'},
            {'Seer'},
            {'Villager'}
        ] + [const.ROLE_SET]*2

        result = algorithms.count_roles(possible_roles_list)

        assert result == {'Seer': 1, 'Villager': 2, 'Wolf': 0}


