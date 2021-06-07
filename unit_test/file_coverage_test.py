""" file_coverage_test.py """
import pprint
from pathlib import Path

IGNORED_FOLDERS = {"__pycache__", "algorithms", "learning", "wolf_variants"}
IGNORED_FILES = {"__init__.py", "gui.py", "log.py"}
wolfbot_FOLDER = Path("wolfbot")
TEST_FOLDER = Path("unit_test")


def test_file_coverage() -> None:
    untested_files = []
    if not wolfbot_FOLDER.is_dir() or not TEST_FOLDER.is_dir():
        raise RuntimeError(f"{wolfbot_FOLDER} and/or {TEST_FOLDER} does not exist.")
    for filepath in wolfbot_FOLDER.rglob("*.py"):
        if (
            filepath.name not in IGNORED_FILES
            and not set(filepath.parts) & IGNORED_FOLDERS
        ):
            partner = TEST_FOLDER / filepath.relative_to(wolfbot_FOLDER)
            partner = partner.with_stem(f"{partner.stem}_test")
            if not partner.is_file():
                untested_files.append((str(filepath), str(partner)))
    assert not untested_files, pprint.pformat(untested_files)
