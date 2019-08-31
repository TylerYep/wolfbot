from src import util
util.print_roles(["hi", "bye"])
print("hiii")

def test_util():
    assert util.print_roles(["hi", "bye"]) == ""