from scipy.optimize import differential_evolution
from flappy import main
import numpy as np

bound = 1
bounds = np.array([(-bound,bound)] * 18)
def tryout(x):
    return -(x**2)

result = differential_evolution(main,bounds,maxiter=20000000, disp=True)
print(result)

# TODO make nicer prints, add options
# TODO save weights and load them
