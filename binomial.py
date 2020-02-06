import numpy as np

# Input variables
K = 99
S0 = 100
r = 0.06
sigma = 0.20
dt = 1 / 50

# Model Parameters
u = np.exp(sigma * np.sqrt(dt))
d = np.exp(-sigma * np.sqrt(dt))
