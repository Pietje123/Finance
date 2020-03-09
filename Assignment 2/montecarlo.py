import numpy as np
from scipy.stats import norm


class MonteCarlo:
    def __init__(self, starting_price, r, T, K, steps, stock_sigma, call=False, digital=False):
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

    def run(self, trials=1, seed=None):
        stock_prices = np.array([self.starting_price] * trials, dtype=np.float64)

        np.random.seed(seed)
        for step in range(self.steps):
            epsilons = np.random.normal(size=trials)
            stock_prices += stock_prices * (self.r * self.dt + self.stock_sigma * epsilons * self.dt ** 0.5)

        payoffs = np.clip((stock_prices - self.K) * (1 if self.call else -1), a_min=0, a_max=None)

        if self.digital:
            payoffs = np.ceil(np.clip(payoffs, a_min=None, a_max=1))

        return payoffs * np.exp(-self.r * self.T)

    def run_immediately(self, trials=1, seed=None):
        stock_prices = np.array([self.starting_price] * trials, dtype=np.float64)

        np.random.seed(seed)
        epsilons = np.random.normal(size=trials)
        stock_prices *= np.exp((self.r - 0.5 * self.stock_sigma**2) * self.T + self.stock_sigma * self.T**0.5 * epsilons)

        payoffs = np.clip((stock_prices - self.K) * (1 if self.call else -1), a_min=0, a_max=None)

        if self.digital:
            payoffs = np.ceil(np.clip(payoffs, a_min=None, a_max=1))

        return payoffs * np.exp(-self.r * self.T)
