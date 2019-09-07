''' fixtures.py '''
from typing import List

def example_game_roles() -> List[str]:
    return ['Villager', 'Seer', 'Robber']

def large_game_roles() -> List[str]:
    return ['Insomniac', 'Villager', 'Wolf', 'Seer', 'Villager', 'Tanner', 'Mason', 'Wolf',
            'Minion', 'Mason', 'Drunk', 'Villager', 'Troublemaker', 'Robber', 'Hunter']

def debug_issues(captured, expected):
    print(len(captured), len(expected))
    for i, captured_char in enumerate(captured):
        if captured_char != expected[i]:
            print("INCORRECT: ", i, captured_char + " vs " + expected[i])
        else:
            print(" " * 10, i, captured_char + " vs " + expected[i])
