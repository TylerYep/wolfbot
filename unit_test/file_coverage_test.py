""" file_coverage_test.py """
import os
import pprint

IGNORED_FOLDERS = {"wolf_variants", "learning", "algorithms"}
IGNORED_FILES = {"log.py", "gui.py"}
SRC_FOLDER = "src"
TEST_FOLDER = "unit_test"


def test_file_coverage() -> None:
    untested_files = []
    if not os.path.isdir(SRC_FOLDER) or not os.path.isdir(SRC_FOLDER):
        raise RuntimeError(f"{SRC_FOLDER} and/or {TEST_FOLDER} does not exist.")
    for root, _, files in os.walk(SRC_FOLDER):
        if set(os.path.normpath(root).split(os.sep)) & IGNORED_FOLDERS:
            continue
        new_root = root.replace(SRC_FOLDER, TEST_FOLDER)
        for filename in files:
            if filename in IGNORED_FILES:
                continue
            basename, ext = os.path.splitext(filename)
            if ext == ".py" and "__" not in filename:
                partner = os.path.join(new_root, basename + "_test.py")
                if not os.path.isfile(partner):
                    untested_files.append((os.path.join(root, filename), partner))
    assert not untested_files, pprint.pformat(untested_files)
