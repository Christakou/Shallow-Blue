# Shallow Blue

A fully working chess-game made in Python ([PyGame](https://www.pygame.org/wiki/GettingStarted)) using the [MinMax algorithm](https://en.wikipedia.org/wiki/Minimax) using Alpha-Beta prunning to reduce the search space of possible moves.

## Introduction
This project aims at creating a playable chess game, by both fully implementing the board environment in PyGame, but also the computer-based agent to play against.

The value function implemented currently is very simplistic and only looks at how many pieces are of each colour and sums their respective value.

We represent the board states as python objects and use the MinMax algorithm to find the best move by looking at the future possible boards that arise from each move.
## Installation
Clone the repo into a new environment and install PyGame.
```
pip install pygame
```
## Future Plans

* Implement a more memory efficient board representation using Numpy arrays
* Implement a more sophisticated evaluation function that is capable of deriving value from positional attributes (bishop pairs, rooks on open files, knights protecting each other etc...)
