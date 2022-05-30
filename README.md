# WolfBot

### One Night Ultimate Werewolf: AI Edition

By Tyler Yep & Harry Sha

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![Build Status](https://github.com/TylerYep/wolfbot/actions/workflows/test.yml/badge.svg)](https://github.com/TylerYep/wolfbot/actions/workflows/test.yml)
[![GitHub license](https://img.shields.io/github/license/TylerYep/wolfbot)](https://github.com/TylerYep/wolfbot/blob/main/LICENSE)
[![codecov](https://codecov.io/gh/TylerYep/wolfbot/branch/main/graph/badge.svg)](https://codecov.io/gh/TylerYep/wolfbot)

## Introduction

This is an implementation of the popular board game One Night Ultimate Werewolf.

To try it out, run `python main.py` in the terminal.
(You may need to run `pip install -r requirements.txt` first.)

Constants, along with their use cases, are listed in wolfbot/const.py. You can change:

- \# of players
- \# of center cards
- Which roles are used
- Behavior of AI players on the Werewolf Team / Village Team

## Interactive Mode

To play the game yourself as a character, use the `-u` / `--user` flag:

```
python main.py --user
```

To replay a game, add the `-r` / `--replay` flag.

```
python main.py --user -r
```

To examine verbose output of a game, use the `-l` / `--log_level` flag.

```
python main.py -l trace
```

## Simulating Games

To simulate many runs of the game, use the `-n` flag.

```
python main.py -n 100
```

or use the profiler:

```
python profiler.py
```

For additional information, please check out the GitHub Wiki!

# Contributing

All issues and pull requests are much appreciated!

- First, run `pre-commit install`.
- To see test coverage scripts and other auto-formatting tools, use `pre-commit run -a`.
- To run all tests, run `pytest`.
- To only run unit tests, run `pytest tests/unit_test`.
- To only run integration tests, run `pytest tests/integration_test`.
