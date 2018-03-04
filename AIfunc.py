from scipy.optimize import rosen, differential_evolution
from flappy import main
import numpy as np


bounds = np.array([(-0.1,0.1)] * 18)
result = differential_evolution(main,bounds,maxiter=20000000, disp=True)