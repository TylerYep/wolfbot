# WolfBot
### One Night Ultimate Werewolf: AI Edition
By Tyler Yep & Harry Sha

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![Build Status](https://travis-ci.org/TylerYep/wolfbot.svg?branch=master)](https://travis-ci.org/TylerYep/wolfbot)
[![GitHub license](https://img.shields.io/github/license/TylerYep/wolfbot)](https://github.com/TylerYep/wolfbot/blob/master/LICENSE)
[![codecov](https://codecov.io/gh/TylerYep/wolfbot/branch/master/graph/badge.svg)](https://codecov.io/gh/TylerYep/wolfbot)
[![DeepSource](https://static.deepsource.io/deepsource-badge-light-mini.svg)](https://deepsource.io/gh/TylerYep/wolfbot/?ref=repository-badge)

## Introduction
This is an implementation of the popular board game One Night Ultimate Werewolf.

To try it out, run `python main.py` in the terminal.
(You may need to run `pip install -r requirements.txt` if you do not have tqdm already installed.)

Constants, along with their use cases, are listed in src/const.py. You can change:
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

For additional information, please check out the GitHub Wiki!


# Contributing
All issues and pull requests are much appreciated!

- To start developing, first run `pip install -r requirements-dev.txt`.
- Next, run 'scripts/install-hooks'.
- To see test coverage scripts and other auto-formatting tools, check out `scripts/run-tests`.
- To run all tests, run `pytest`.
- To only run unit tests, run `pytest unit_test`.
- To only run integration tests, run `pytest integration_test`.
