from scipy.optimize import differential_evolution
import numpy as np
from game import Game

bound = 3
bounds = np.array([(-bound,bound)] * 18)
game = Game(MANUAL_PLAY = False)
result = differential_evolution(game.main ,bounds,maxiter=20000000, disp=True)
print(result)

# TODO make nicer prints, add options
# TODO save weights and load them
