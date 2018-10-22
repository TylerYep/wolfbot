# WolfBot
### One Night Ultimate Werewolf: AI Edition
By Tyler Yep and Harry Sha

To try it out, run 'python src/main.py' in the terminal. (Python 3.7)  
Constants, along with their use cases, are listed in src/const.py.

# Development
## October 2018
More Wolf updates - I updated the Expectimax algorithm and changed the statements
Wolves use. Fully tested all Wolf types and finished Pylint refactoring.


## September 2018
Major refactoring update and Single-Wolf Voting added! The next primary focus will be on
getting a conversation between roles - each character has more than one statement and is
able to convey different types of information. This will enable us to give varying confidence
levels to Wolf accusations, and even allow us to add more evil roles, like the Tanner and
Minion. By rough estimate, with 12 roles, there are roughly 250 million different games that
can occur (role assignments, and then switching scenarios). This is sufficient reason to
develop AI that can face this challenge, and the introduction of multiple statements will
only push this number higher.


## June 2018
Presented the final iteration of the project at the CS 221 Project Fair. Good feedback
overall, main points moving forward may be looking into using the minimum expectation
for the Wolf players, adding new statements from each player (more than one round of speaking),
and adding wildcard characters like Minions and Tanners. More to come!


## May 2018
Much progress has been made after only a week of working on this project.

Our main update was introducing the Wolf AI to the mix. The goal here is to develop
the two AI in parallel - every time the Good players get smarter, the Wolves gain
more trickery and better plans. Each AI has access to the same solvers, and as such
can run their own games and gain their own experience to make better predictions.
Entirely possible the AI players get so smart they develop their own game meta that
humans cannot logically understand, but that hasn't happened yet, so we're fine.

Harry introduced the Expectimax Wolf player, which after my modification to the
set of statements it considers, functions extremely well in avoiding detection, and
finishes running with decent efficiency over 1000 iterations.


## April 2018
First thoughts to make an AI that can play a game of One Night Ultimate Werewolf.
Developed as part of a project for Stanford's CS 221: Artificial Intelligence course.
Main focus for this project is on incremental development, introducing new roles and new
game mechanics slowly to ensure all scenarios are covered and interpreted optimally.

First steps were to recreate a simplified version of game in Python. We initially only
used 5 characters in the game: Villager (x3), Wolf (x2), and Seer. In one_night.py,
we randomly assign roles from const.py, have night fall, and then have each character
give a statement about what they did during the night. Emphasis on making code expand
naturally, minimizing refactoring.

Next, we made a solver for a set of statements from each player. Majority of
the work here goes to Harry for introducing a Consistency verifier for Statements,
and creating the Baseline Solver.


# Files
## Game Simulation
* const.py (Stores all constants, along with their use cases)  
* main.py (Driver for game simulations)  
* one_night.py (Plays one game of One Night Ultimate Werewolf)  
* statistics.py (Used to aggregate many GameResults into fixed statistics)  
* replay.py (python3 src/replay.py will run the last game that was played again)  
* encoder.py (Used to encode all custom WolfBot class objects)  

## Algorithms and Solvers
* algorithms.py (Includes all solvers and consistency checks for groups of statements)  
* generate.py (Used to generate data for many game iterations)  
* possible.py (Finds all possible player statements for Wolves)  
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

TODO:
* Host on AWS (SOON)
* UI and secure move API
* Multiple Statements
* Add Minion
* Add Tanner!

Pylint entire directory using:
find . -iname "*.py" | xargs pylint
