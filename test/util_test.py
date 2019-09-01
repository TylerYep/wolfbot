''' util_test.py '''
from src import util

def test_print_roles(caplog):
    ''' util_test.py '''
    expected = '[Hidden] Current roles: [hi, bye]                 \n\t  Center cards: []\n'
    util.print_roles(["hi", "bye"])
    captured = caplog.records[0].getMessage()
    assert captured == expected


def debug_issues(captured, expected):
    ''' util_test.py '''
    print(len(captured), len(expected))
    for i, captured_char in enumerate(captured):
        if captured_char != expected[i]:
            print("INCORRECT: ", i, captured_char + " vs " + expected[i])
        else:
            print(" " * 10, i, captured_char + " vs " + expected[i])
