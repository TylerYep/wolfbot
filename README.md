# WolfBot
### One Night Ultimate Werewolf: AI Edition
By Tyler Yep & Harry Sha

To try it out, run 'python src/main.py' in the terminal. (Python 3.7)  
Constants, along with their use cases, are listed in src/const.py.

# Development

## September 2019



## August 2019
Started working on this project again. The main blocker for adding more functionality is the lack of testing I currently have. Without solid unit/integration tests, it's really easy to break or change existing functionality silently. So, I have decided to begin using Pytest as a framework for writing unit tests for the existing code. The test/ folder is intended to follow the folder structure of src/, and will import accordingly. To accomplish this change, I had to change many of the imports to explicitly start from src/. Additionally, to aid this effort, I have also decided to introduce type annotations for all function declarations, which will make the test writing process a lot easier. I use Facebook's Pyre as a fast type checker, which together with Pylint has helped me find and fix a lot of poor design decisions in my code.


## July 2019
Changed all interpolated strings in this project to use f-strings, which are intended to be much more performant and readable, even in logging scenarios.


## January 2019
Interactive mode and Hunter added!


## December 2018
Added the Minion and Tanner characters and fully integrated them into the game! I changed a large portion of how voting works and how possible statements are obtained (now, saying you are a Wolf is not necessarily a bad idea). I have a lot more ideas to move forward with as well - for example, drawing out file dependencies and finding better representations, using some unit testing to make sure everything works as expected before expanding the game, and using the new Python 3.7 type-checking. Overall, the game looks like it's in a stable state, and the Werewolf and Tanner teams look like they have the advantage. Time to start thinking of more advanced Village team tactics!


## November 2018
Started the basic framework for the Minion. Currently working on other projects, so I will return to this project later.


## October 2018
More Wolf updates - I updated the Expectimax algorithm and changed the statements Wolves use. Fully tested all Wolf types and finished Pylint refactoring.


## September 2018
Major refactoring update and Single-Wolf Voting added! The next primary focus will be on getting a conversation between roles - each character has more than one statement and is able to convey different types of information. This will enable us to give varying confidence levels to Wolf accusations, and even allow us to add more evil roles, like the Tanner and Minion. By rough estimate, with 12 roles, there are roughly 250 million different games that can occur (role assignments, and then switching scenarios). This is sufficient reason to develop AI that can face this challenge, and the introduction of multiple statements will only push this number higher.


## June 2018
Presented the final iteration of the project at the CS 221 Project Fair. Good feedback
overall, main points moving forward may be looking into using the minimum expectation
for the Wolf players, adding new statements from each player (more than one round of speaking),
and adding wildcard characters like Minions and Tanners. More to come!


## May 2018
Much progress has been made after only a week of working on this project.

Our main update was introducing the Wolf AI to the mix. The goal here is to develop the two AI in parallel - every time the Good players get smarter, the Wolves gain more trickery and better plans. Each AI has access to the same solvers, and as such can run their own games and gain their own experience to make better predictions. Entirely possible the AI players get so smart they develop their own game meta that humans cannot logically understand, but that hasn't happened yet, so we're fine.

Harry introduced the Expectimax Wolf player, which after my modification to the set of statements it considers, functions extremely well in avoiding detection, and finishes running with decent efficiency over 1000 iterations.


## April 2018
First thoughts to make an AI that can play a game of One Night Ultimate Werewolf. Developed as part of a project for Stanford's CS 221: Artificial Intelligence course. Main focus for this project is on incremental development, introducing new roles and new game mechanics slowly to ensure all scenarios are covered and interpreted optimally.

First steps were to recreate a simplified version of game in Python. We initially only used 5 characters in the game: Villager (x3), Wolf (x2), and Seer. In one_night.py, we randomly assign roles from const.py, have night fall, and then have each character give a statement about what they did during the night. Emphasis on making code expand naturally, minimizing refactoring.

Next, we made a solver for a set of statements from each player. Majority of the work here goes to Harry for introducing a Consistency verifier for Statements, and creating the Baseline Solver.

# Developer Commands
* For truly deterministic results during testing, run
```
PYTHONHASHSEED=0 python src/main.py
```
and make sure const.py sets the random seed.

* Pylint entire directory using:
```
pylint
find . -iname "*.py" | xargs pylint
```
* Type-check the directory using Pyre:
```
pyre check
```

# Files
## Game Simulation
* const.py (Stores all constants, along with their use cases)  
* main.py (Driver for game simulations)  
* one_night.py (Plays one game of One Night Ultimate Werewolf)  
* statistics.py (Used to aggregate many GameResults into fixed statistics)  
* replay.py (python src/replay.py will run the last game that was played again)  
* encoder.py (Used to encode all custom WolfBot class objects)  

## Algorithms and Solvers
* algorithms.py (Includes all solvers and consistency checks for groups of statements)  
* generate.py (Used to generate data for many game iterations)  
* predictions.py (Makes predictions given a SolverSolution)  
* train.py (Used for Reinforcement Learning Wolf)  
* voting.py (Used to aggregate prediction results)  

## Game Components
* roles.py (Stores all Good player roles and their associated methods)  
  (May separate into individual files in the future)  
* wolf.py (Stores all Evil player roles and their associated methods)  
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

# Future Development Todos
* Host on AWS
* UI and secure move API
* Multiple Statements
* Unit testing
* Player can accept 0 parameters? just multiply to make list.
* Wolf_inds isn't used in stats

# File Dependency Tree
Simplified version (some cycles exist)  

src/

const.py  
|-- predictions.py  
|-- statistics.py  
|-- statements.py  
|-- util.py  
|   |-- algorithms.py   (const, statements)  
|   |-- roles/          (const, statements, util)  
|   |   |-- main.py           (algorithms, const, one_night, statistics)  
|   |   |-- generate.py       (algorithms, encoder, const, one_night)  
|   |   |-- encoder.py        (const, roles, statements, statistics)  
|   |   |   |-- one_night.py        (const, encoder, roles, voting, util)  
|   |   |   |-- replay.py           (algorithms, const, encoder, prediction, statistics, voting)  
|   |   |   |-- train.py            (encoder, main)  
|   |   |   |-- voting.py           (const, roles, statements, statistics)  

roles/        (imports const, statements, util)  

villager/  
player.py  
|-- drunk.py  
|-- insmoniac.py (imports wolf in get_statements)  
|-- mason.py  
|-- robber.py (imports wolf in get_statements)  
|-- seer.py  
|-- troublemaker.py  
|-- villager.py  

werewolf/ (imports player, villager)  
|-- minion.py  
|-- wolf.py (imports wolf in get_statements)  
|   |-- center_wolf.py  
|   |-- expectimax_wolf.py  
|   |-- random_wolf.py  
|   |-- reg_wolf.py  
|   |-- rl_wolf.py  
