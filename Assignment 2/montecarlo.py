import numpy as np
from scipy.stats import norm
import numpy as np


class MonteCarlo:
    def __init__(self, starting_price, r, T, K, steps, stock_sigma, call=True, digital=False, seed=None):
        self.starting_price = starting_price
        self.stock_sigma = stock_sigma
        self.r = r
        self.T = T
        self.K = K
        self.steps = steps
        self.dt = T/steps
        self.t = 0
        self.call = call
        self.digital = digital
        self.seed = seed

    def run(self, trials=1):
        stock_prices = np.array([self.starting_price] * trials, dtype=np.float64)

        for step in range(self.steps):
            np.random.seed(self.seed)
            epsilons = np.random.normal(size=trials)
            stock_prices += stock_prices * (self.r * self.dt + self.stock_sigma * epsilons * self.dt ** 0.5)

        payoffs = np.clip((stock_prices - self.K) * (1 if self.call else -1), 0, (1 if self.digital else None))
        return payoffs * np.exp(-self.r * self.T)
