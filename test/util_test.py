from src import util

def test_print_roles(caplog):
    expected = '[Hidden] Current roles: [hi, bye]                 \n\t  Center cards: []\n'
    util.print_roles(["hi", "bye"])
    captured = caplog.records[0].getMessage()
    assert captured == expected


def debug_issues(captured, expected):
    print(len(captured), len(expected))
    for char in range(len(captured)):
        if captured[char] != expected[char]:
            print("INCORRECT: ", char, captured[char] + " vs " + expected[char])
        else:
            print(" " * 10, char, captured[char] + " vs " + expected[char])