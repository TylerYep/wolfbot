''' conftest.py '''
from typing import List
import pytest

@pytest.fixture
def example_game_roles() -> List[str]:
    return ['Villager', 'Seer', 'Robber']

@pytest.fixture
def large_game_roles() -> List[str]:
    return ['Wolf', 'Villager', 'Robber', 'Seer', 'Villager', 'Tanner', 'Mason', 'Wolf',
            'Minion', 'Mason', 'Drunk', 'Villager', 'Troublemaker', 'Insomniac', 'Hunter']

# from src import const
# @pytest.fixture(autouse=True)
# def reset_const():
#     const.ROLES = ('Insomniac', 'Villager', 'Villager', 'Villager', 'Drunk', 'Wolf', 'Wolf', 'Seer',
#                    'Tanner', 'Mason', 'Mason', 'Troublemaker', 'Robber', 'Minion', 'Hunter')
#     const.logger.setLevel(const.TRACE)

def debug_spacing_issues(captured, expected):
    ''' Helper method for debugging print differences. '''
    print(len(captured), len(expected))
    for i, captured_char in enumerate(captured):
        if captured_char != expected[i]:
            print("INCORRECT: ", i, captured_char + " vs " + expected[i])
        else:
            print(" " * 10, i, captured_char + " vs " + expected[i])