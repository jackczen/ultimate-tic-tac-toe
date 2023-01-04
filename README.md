
# Ultimate Tic-Tac-Toe

## Overview
This repository provides a suite of scripts for benchmarking, visualizing, and playing against [MiniMax](https://en.wikipedia.org/wiki/Minimax) artificial intelligence agents in the game of [Ultimate Tic-Tac-Toe](https://en.wikipedia.org/wiki/Ultimate_tic-tac-toe).

## Usage
To run the primary script, execute the command
```
python game.py
```
To specify the agent type of Player X, use the option `-x`. Likewise, use the option `-o` to specify the agent type of Player O. Currently, the supported agent types are `RandomAgent`, `HumanAgent`, and `MiniMaxAgent`.

If the `HumanAgent` type is specified, the graphical interface will be displayed automatically so that the user can make moves. However, to visualize a game between any two agents, use the flag `-g`.

To run simulate several games successively, use the option `-n`.

### MiniMaxAgent
Each `MiniMaxAgent` has an [evaluation functions](https://en.wikipedia.org/wiki/Evaluation_function) and a search depth. The evaluation function for Player X can be specified by the option `--xe`, and the evaluation function for Player O can be specified by the option `--oe`. The currently supported evaluation functions are
```
count_wins                  Sums the values of terminal sub-boards, where X wins are valued as 
                            +1, O wins are valued as -1, and ties are valued as 0.

cell_weight_evaluation      Computes a weighted sum of terminal sub-boards; each sub-board is 
                            weighted by the number of possible wins that they can contribute to 
                            (for instance, the middle sub-board has a weight of 4, since it 
                            can contribute to winning once vertically, winning once 
                            horizontally,and winning twice diagonally); X wins are valued as 
                            +1, O wins are valued as -1, and ties are valued as 0.

near_wins                   Sums the number of “near-wins,” instances where two of the three 
                            necessary pieces are placed to win, in the large board; X 
                            near-wins are weighted as +1, and O near-wins are weighted as -1.

nested_near_wins            Sums the computation of near_wins on both the large board and 
                            each individual sub-board; near-wins in the sub-boards are weighted 
                            such that, if every sub-board has the maximum number of near-wins 
                            (6), the total sum is weighted less than one near-win on the large 
                            board.

shallow_simple_evaluation   Sums the number of “near-wins” and “semi-near-wins,” defined as one
                            piece in line with two empty cells, in the large board; near-wins 
                            are valued ten times more than semi-near-wins, and each is 
                            multiplied by +1 if it belongs to X, -1 if it belongs to O.

deep_simple_evaluation      Sums the “shallow_simple_evaluation” executed on the large board 
                            and all non-terminal sub-boards. Near-wins in the sub-boards are 
                            weighted such that, if every sub-board has the maximum number of 
                            near-wins (6), the total sum is weighted less than one near-win on 
                            the large board.

zero                        Returns 0.
```

To specify the search depth, use the option `--xd` for Player X and `--od` for Player O.

## Extension
### Evaluation Functions
Since Ultimate Tic-Tac-Toe is a [zero sum game](https://en.wikipedia.org/wiki/Zero-sum_game), all evaluation functions must be centered symmetrically around zero. 

To add a new evaluation function for the `MiniMaxAgent`, define a new function in the `evaluation_functions.py` file that takes an instance of `UltimateTicTacToe` as an argument and returns a value in the open interval `(-100, 100)`. The newly defined evaluation function will automatically become a command line option.

### Agents
All game-playing agents must be extend the `Agent` class and be defined in the `agents.py` file. The new class will automatically become a command line option. However, any additional options for the class must be added manually to the parser defined in `game.py`.
