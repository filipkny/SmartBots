Small project where we try to solve Flappy Bird using scipy's differential evolution algorithm.

The game script was originally created by sourabhv (https://github.com/sourabhv/FlapPyBird) and was refractored 
for clarity and modularity (although it is still a bit messy). The game has been divided into a Game class where and instance of the Player class plays.

In Simulation.py we have the function to which all the differential evolution parameters are given and also where we set up to which file the data from each run is saved. For more information on these please look into https://docs.scipy.org/doc/scipy-0.17.0/reference/generated/scipy.optimize.differential_evolution.html

In main.py we have two basic functions, one for running several simulations with different kinds of parameters, and another one for saving an average score/2000 runs graph. If you just want to run one simulation, dont change anything.

Dependencies (they are all included in venv, so you should be able to just download and run it):
* Numpy
* Scipy
* Matplotlib
* Pygame

Results:
* We weren't able to find an optimal solution for PIPEGAPSIZE = 100. Some runs managed to achieve impressive results like (47) but they usually took a very long to get that far.
* For PIPEGAPSIZE = 125 the algorithm converges rather quickly to an optimal solution.

