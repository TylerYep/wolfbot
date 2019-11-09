# WolfBot
### One Night Ultimate Werewolf: AI Edition
By Tyler Yep & Harry Sha

To try it out, run `python main.py` in the terminal. (Python 3.7)  
Constants, along with their use cases, are listed in src/const.py.

# Development
## November 2019
Moving some directories around, with the goal of making it simple to run WolfBot configs and commands from a single client-facing Python script, and being more intentional about client-facing exports. Added a pre-commit git hook to run unit and integration tests before every commit. Tried the cached solver again, framed as the 0-1 knapsack problem, but ran into two difficulties: I have to use a top-down approach because I cannot enumerate all possible states (I don't have weights), and I have to explore separate cases for when a statement is added vs negated and added. Ultimately a dead end, but I still think there's some optimizations to be done.

Experimented with fixtures in other files and randomizing integration tests.


## October 2019
Still testing, working on the tail end parts of the game (predictions, encoder, and voting). Redid the role initialization yet again using the class method decorator to follow more Pythonic conventions. I also added docstrings and the static method decorator to all test file methods to finally silence all of those Pylint warnings.


## September 2019
Spent a bunch of time setting up test stubs and preliminary tests for all files in the project. Getting ever so slightly closer to the goal of knowing when parts of this project is broken and being able to better notate the requirements and design decisions behind some of this code.

In writing so many tests, I've already found a bunch of important improvements and bugs; for example, making the Statement and SolverState classes immutable, since when operating with them, I never want to modify an existing state, but rather always return a new one. I made their constructors take lists and sets as input and automatically convert them to tuples or frozen sets, echoing some of the enhanced Redux state design patterns I've seen, thus making constructing a new state easy.


## August 2019
Started working on this project again. The main blocker for adding more functionality is the lack of testing I currently have. Without solid unit/integration tests, it's really easy to break or change existing functionality silently. So, I have decided to begin using Pytest as a framework for writing unit tests for the existing code. The test/ folder is intended to follow the folder structure of src/, and will import accordingly. To accomplish this change, I had to change many of the imports to explicitly start from src/.

Additionally, to aid this effort, I have also decided to introduce type annotations for all function declarations (return-type and parameter-type annotations), which I believe will make the test writing process a lot easier. I decided to use Facebook's Pyre as a fast type checker, which together with Pylint has helped me find and fix a lot of poor design decisions in my code.


## July 2019
Changed all interpolated strings in this project to use f-strings, which are intended to be much more performant and readable, even in logging scenarios.


## March 2019
Tried using a Dynamic Programming or Greedy Algorithm for switching solver, but it wasn't too successful. I'm not 100% sure that the greedy approach to consistent statement selection works all of the time.


## February 2019
New features! Made Multi-Statement semi-stable, but right now all roles just ignore the extra information given before the final statement. Ideas for big integration testing - I could have a fixed accuracy threshold needed to pass each test when certain features like Expectimax Wolf or Multi-Statement are enabled. I would also love to have different confidence levels for each character, like a probability distribution or something.


## January 2019
Interactive Mode and Hunter added! Working on multiple statements next, but I need to plan it out a bit more before I try to implement it. I plan to branch off of master to get a proof-of-concept working first.


## December 2018
Added the Minion and Tanner characters and fully integrated them into the game! I changed a large portion of how voting works and how possible statements are obtained (now, saying you are a Wolf is not necessarily a bad idea). I have a lot more ideas to move forward with as well - for example, drawing out file dependencies and finding better representations, using some unit testing to make sure everything works as expected before expanding the game, and using the new Python 3.7 type-checking. Overall, the game looks like it's in a stable state, and the Werewolf and Tanner teams look like they have the advantage. Time to start thinking of more advanced Village team tactics!


## November 2018
Started the basic framework for the Minion character. Currently working on other projects, so I will return to this project later.


## October 2018
More Wolf updates - I updated the Expectimax algorithm and changed the statements Wolves use. Fully tested all Wolf types and finished Pylint refactoring.


## September 2018
Major refactoring update and Single-Wolf Voting added! The next primary focus will be on getting a conversation between roles - each character has more than one statement and is able to convey different types of information. This will enable us to give varying confidence levels to Wolf accusations, and even allow us to add more evil roles, like the Tanner and Minion. By rough estimate, with 12 roles, there are roughly 250 million different games that can occur (role assignments, and then switching scenarios). This is sufficient reason to develop AI that can face this challenge, and the introduction of multiple statements will only push this number higher.


## June 2018
Presented the final iteration of the project with Harry at the CS 221 Project Fair. Good feedback overall, main points moving forward may be looking into using the minimum expectation for the Wolf players, adding new statements from each player (more than one round of speaking), and adding wildcard characters like Minions and Tanners. More to come!


## May 2018
Much progress has been made after only a week of working on this project.

Our main update was introducing the Wolf AI to the mix. The goal here is to develop the two AI in parallel - every time the Good players get smarter, the Wolves gain more trickery and better plans. Each AI has access to the same solvers, and as such can run their own games and gain their own experience to make better predictions. Entirely possible the AI players get so smart they develop their own game meta that humans cannot logically understand, but that hasn't happened yet, so we're fine.

Harry introduced the Expectimax Wolf player, which after my modification to the set of statements it considers, functions extremely well in avoiding detection, and finishes running with decent efficiency over 1000 iterations.


## April 2018
First thoughts to make an AI that can play a game of One Night Ultimate Werewolf. Developed as part of a project for Stanford's CS 221: Artificial Intelligence course. Main focus for this project is on incremental development, introducing new roles and new game mechanics slowly to ensure all scenarios are covered and interpreted optimally.

First steps were to recreate a simplified version of game in Python. We initially only used 5 characters in the game: Villager (x3), Wolf (x2), and Seer. In one_night.py, we randomly assign roles from const.py, have night fall, and then have each character give a statement about what they did during the night. Emphasis on making code expand naturally, minimizing refactoring.

Next, we made a solver for a set of statements from each player. Majority of the work here goes to Harry for introducing a Consistency verifier for Statements, and creating the Baseline Solver.


# Results (October 2019):
ROLES = ('Robber', 'Drunk', 'Wolf', 'Troublemaker', 'Seer', 'Minion')
NUM_CENTER = 2
|                 | Sample Size | Accuracy | Any Center | Villager Win Rate | Werewolf Win Rate |
|-----------------|------------:|---------:|-----------:|------------------:|------------------:|
| Random Wolf     |       10000 |    0.644 |      0.674 |             0.505 |             0.494 |
| Regular Wolf    |       10000 |    0.542 |      0.575 |             0.471 |             0.529 |
| Expectimax Wolf |        1000 |    0.615 |      0.648 |             0.467 |             0.533 |


# Developer Commands
* For truly deterministic results during testing, run:
```
PYTHONHASHSEED=0 python main.py
```
Make sure const.py sets the random seed.

* Pylint entire directory using:
```
pylinta
find . -iname "*.py" | xargs pylint
find . -iname "*.py" ! -iname "*_test.py" | xargs pylint
```

* Pylint all test files using:
```
pylinta test
find . -iname "*_test.py" | xargs pylint
```

* Type-check the directory using Pyre:
```
pyre check
```
* Run all tests:
```
pytest -vv [-s to see print/logging output] [unit_test/ or integration_test/]
```

# Style Guidelines
- Tests use the arrange-act-assert paradigm with one line break in between each.
- Tests do not need docstrings or return types, but every other .py file should annotate return types and parameter types. Can use inline code types wherever useful, but those are optional.
- Imports go builtins, empty space, other imports, then relative imports. Typing imports are arranged in alphabetical order.

# Files
## Game Simulation
* const.py (Stores all constants, along with their use cases)
* main.py (Driver for game simulations)
* one_night.py (Plays one game of One Night Ultimate Werewolf)
* stats.py (Used to aggregate many GameResults into fixed statistics)
* replay.py (`python main.py -r` will replay the most recently run game)
* encoder.py (Used to encode all custom WolfBot class objects)

## Algorithms and Solvers
* algorithms.py (Includes all solvers and consistency checks for groups of statements)
* generate.py (Used to generate data for many game iterations)
* predictions.py (Makes predictions given a SolverSolution)
* train.py (Used for Reinforcement Learning Wolf)
* voting.py (Used to aggregate prediction results)

## Game Components
* roles/
  * village (Stores all good player roles and their associated methods)
  * werewolf (Stores all evil player roles and their associated methods)
* statements.py (Statement class with associated methods)
* util.py (Some basic util functions)

## Roles
Village Team: (Stores all Good player roles and their associated methods)
* Villager
* Mason
* Seer
* Robber
* Troublemaker
* Drunk
* Insomniac

Werewolf Team: (Stores all Evil player roles and their associated methods)
* Wolf
* Minion

Tanner Team: (Wildcard player)
* Tanner

Wolf Theory: Choose statements that do a good job, not necessarily the absolute best ones.

# File Dependency Tree
Simplified version (some cycles exist)

#### src/
```
main.py         (const, algorithms, one_night, stats)
const.py        ()
|-- statements.py   (const)
|-- util.py         (const)
|   |-- algorithms.py   (const, statements)
|   |-- roles/          (const, statements, util)
|   |   |-- stats.py          (const, roles, statements)
|   |   |   |-- predictions.py    (const, algorithms)
|   |   |   |-- generate.py       (const, algorithms, one_night, encoder)
|   |   |   |-- encoder.py        (const, roles, statements, stats)
|   |   |   |   |-- one_night.py        (const, util, roles, encoder, voting)
|   |   |   |   |-- replay.py           (const, algorithms, encoder, prediction, stats, voting)
|   |   |   |   |-- train.py            (encoder, main)
|   |   |   |   |-- voting.py           (const, roles, statements, stats)
```
#### roles/villager/
```
player.py
|-- drunk.py
|-- insmoniac.py (imports wolf in get_statements)
|-- mason.py
|-- robber.py (imports wolf in get_statements)
|-- seer.py
|-- troublemaker.py
|-- villager.py
```
#### roles/werewolf/         (player, villager)
```
|-- minion.py
|-- wolf.py (imports wolf in get_statements)
|   |-- center_wolf.py
|   |-- expectimax_wolf.py
|   |-- random_wolf.py
|   |-- reg_wolf.py
|   |-- rl_wolf.py
```

# Future Development Todos
* Big Directional Goals:
  * Host on AWS
  * UI and secure move API
  * Multiple Statements
  * Predictions with constraint satisfaction heuristics: https://simpleai.readthedocs.io/en/latest/constraint_satisfaction_problems.html

* Unit Testing:
  * Wolf_inds isn't used in stats.py
  * Insomniac testing is very confusing to me.
  * Test constructors more thoroughly.
  * Make_prediction needs more thorough testing.
  * Should all object constructors take in a list and convert it to a tuple manually, for easy JSONing?

* Design Considerations:
  * game_roles and original_roles in the classes for each role: different for each awake_init function? Causes a lot of pylint issues. I could find how many to pass in one_night.
  * Rethink Wolf characters and how the class mechanics work before writing their tests. This may be the next big step in the project, or I might go back to multi-statement.
  * Should have statements on init like all of the other characters. The reason I didn't originally was to trim the set using previous statements.
  * new_role should be a learnable vector or a dict that gets updated as the probability of change increases.
  * Creating a directed statement index dependency graph to use in conjunction with the solver. Find the hubs and find statements that don't connect very much with the graph.

* Small Stories:
  * Make train.py run from main.py
  * better eval function for minion / tanner / wolf
