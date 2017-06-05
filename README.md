# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?
A: In the naked twins problem we add the following constraint to the system. If a box inside the board contains only two possible solutions, and there exists a box within its peers that also contains the same two possible solutions, then these two boxes are said to be "naked twins".

If the naked twins lie on the same column, the constraint can be propagated to the other boxes in the same column by eliminating the two "twin" solutions from their possible set of solutions. The same process can be done to row boxes if the twins lie on the same row. Since the two possible solutions apply to both of the twin boxes, as soon as one is defined with one of the two values, the other must be set to the remaining value.

It is possible for one box to have two naked twins. One naked twin on its row and one on its column.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?
A: The diagonal sudoku adds an additional constraint to the original sudoku. In this modified version, boxes that belong to one of the two diagonals on the board will belong to a new unit of boxes, i.e. the diagonal of boxes. The previous algorithms of search, only choice and eliminate can be run unchanged since the only modification that is needed is the addition of these two new diagonal units.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project.
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.
