import numpy as np
from scipy.stats import norm


class Path:
    def __init__(self, starting_price, stock_sigma, hedge_sigma, r, T, K, steps, hedge_interval):
        self.stock_price = starting_price
        self.stock_sigma = stock_sigma
        self.hedge_sigma = hedge_sigma
        self.r = r
        self.T = T
        self.K = K
        self.steps = steps
        self.hedge = 0
        self.dt = T/steps
        self.t = 0
        self.hedge_interval = hedge_interval
        d1 = 1 / (self.hedge_sigma * np.sqrt(T)) * (np.log(self.stock_price / K) + (r + ((self.hedge_sigma ** 2) / 2)) * T)
        d2 = d1 - (hedge_sigma * np.sqrt(T))
        self.profit = norm.cdf(d1) * self.stock_price - norm.cdf(d2) * K * np.exp(-r * (T))

    def update_price(self):
        epsilon = np.random.normal()
        self.stock_price += self.stock_price * (self.r * self.dt + self.stock_sigma * epsilon * self.dt ** 0.5)

    def update_hedge(self):
        d1 = 1 / (self.hedge_sigma * np.sqrt(self.T - self.t)) * (np.log(self.stock_price / self.K) + (self.r + ((self.hedge_sigma ** 2) / 2)) * (self.T - self.t))
        self.hedge = norm.cdf(d1)

    def run(self):
        self.update_hedge()
        self.profit -= self.hedge * self.stock_price

        for step in range(self.steps):
            self.profit = self.profit * np.exp(self.r * self.dt)
            self.update_price()
            if (step % self.hedge_interval) == 0 and step < self.steps-1:
                self.profit += self.hedge * self.stock_price
                self.update_hedge()
                self.profit -= self.hedge * self.stock_price

        if self.stock_price > self.K:
            self.profit -= (1 - self.hedge) * self.stock_price
            self.profit += self.K
        else:
            self.profit += self.hedge * self.stock_price

        return self.profit