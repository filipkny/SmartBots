from scipy.optimize import differential_evolution
import numpy as np
from game import Game

bound = 10
good_start = [ 0.42808821, -2.20599695, -1.36463635, -2.64356078, -0.3414663 ,
        1.54710738, -2.42923382,  0.69040533, -1.59005237,  2.78380053,
       -2.25658969,  0.99114311, -2.482751  , -1.89836315,  0.51885838,
        0.7911339 ,  0.79377306, -1.64218754]

bounds = np.array([(-bound,bound)] * 18)
game = Game(MANUAL_PLAY = False)
result = differential_evolution(game.main ,bounds,maxiter=20000000, disp=True)
print(result)

# TODO make nicer prints, add options
# TODO save weights and load them
