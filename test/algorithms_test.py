''' algorithms_test.py '''
# from src import algorithms
# from src.statements import Statement
#
# def test_switching_solver(caplog):
#     STATEMENT_LIST = [
#         Statement('I am a Robber and I swapped with Player 6. I am now a Drunk.',
#                   [(0, {'Robber'}), (6, {'Drunk'})], [(0, 6, 0)]),
#         Statement('I am a Robber and I swapped with Player 0. I am now a Seer.',
#                   [(1, {'Robber'}), (0, {'Seer'})], [(0, 0, 1)]),
#         Statement('I am a Seer and I saw that Player 3 was a Villager.',
#                   [(2, {'Seer'}), (3, {'Villager'})], []),
#         Statement('I am a Villager.', [(3, {'Villager'})], []),
#         Statement('I am a Mason. The other Mason is Player 5.',
#                   [(4, {'Mason'}), (5, {'Mason'})], []),
#         Statement('I am a Mason. The other Mason is Player 4.',
#                   [(5, {'Mason'}), (4, {'Mason'})], []),
#         Statement('I am a Drunk and I swapped with Center 1.',
#                   [(6, {'Drunk'})], [(1, 9, 6)]),
#         Statement('I am a Robber and I swapped with Player 5. I am now a Seer.',
#                   [(7, {'Robber'}), (5, {'Seer'})], [(0, 5, 7)])
#     ]
#
#     result = algorithms.switching_solver(STATEMENT_LIST)
#
#     expected_possible_roles = [
#         {'Robber'},
#         {'Seer', 'Hunter', 'Drunk', 'Tanner', 'Wolf', 'Insomniac',
#         'Mason', 'Minion', 'Villager', 'Troublemaker'},
#         {'Seer'},
#         {'Villager'},
#         {'Mason'},
#         {'Mason'},
#         {'Drunk'},
#         {'Seer', 'Hunter', 'Drunk', 'Tanner', 'Wolf', 'Insomniac', 'Mason',
#         'Minion', 'Villager', 'Troublemaker'},
#         {'Seer', 'Hunter', 'Drunk', 'Tanner', 'Robber', 'Wolf', 'Insomniac',
#         'Mason', 'Minion', 'Villager', 'Troublemaker'},
#         {'Seer', 'Hunter', 'Drunk', 'Tanner', 'Robber', 'Wolf', 'Insomniac',
#         'Mason', 'Minion', 'Villager', 'Troublemaker'},
#         {'Seer', 'Hunter', 'Drunk', 'Tanner', 'Robber', 'Wolf', 'Insomniac',
#         'Mason', 'Minion', 'Villager', 'Troublemaker'},
#         {'Seer', 'Hunter', 'Drunk', 'Tanner', 'Robber', 'Wolf', 'Insomniac',
#         'Mason', 'Minion', 'Villager', 'Troublemaker'},
#         {'Seer', 'Hunter', 'Drunk', 'Tanner', 'Robber', 'Wolf', 'Insomniac',
#         'Mason', 'Minion', 'Villager', 'Troublemaker'},
#         {'Seer', 'Hunter', 'Drunk', 'Tanner', 'Robber', 'Wolf', 'Insomniac',
#         'Mason', 'Minion', 'Villager', 'Troublemaker'},
#         {'Seer', 'Hunter', 'Drunk', 'Tanner', 'Robber', 'Wolf', 'Insomniac',
#         'Mason', 'Minion', 'Villager', 'Troublemaker'}
#     ]
#     expected_path = [True, False, True, True, True, True, True, False]
#     assert result[0].possible_roles == expected_possible_roles
#     assert result[0].path == expected_path
