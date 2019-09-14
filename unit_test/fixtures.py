''' fixtures.py '''
from typing import List

def example_game_roles() -> List[str]:
    return ['Villager', 'Seer', 'Robber']

def large_game_roles() -> List[str]:
    return ['Wolf', 'Villager', 'Robber', 'Seer', 'Villager', 'Tanner', 'Mason', 'Wolf',
            'Minion', 'Mason', 'Drunk', 'Villager', 'Troublemaker', 'Insomniac', 'Hunter']

def debug_issues(captured, expected):
    print(len(captured), len(expected))
    for i, captured_char in enumerate(captured):
        if captured_char != expected[i]:
            print("INCORRECT: ", i, captured_char + " vs " + expected[i])
        else:
            print(" " * 10, i, captured_char + " vs " + expected[i])
