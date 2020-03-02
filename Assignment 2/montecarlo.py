import numpy as np
from scipy.stats import norm
import numpy as np

class Path:
    def __init__(self, starting_price, r, T, K, steps, stock_sigma):
        self.stock_price = starting_price
        self.stock_sigma = stock_sigma
        self.r = r
        self.T = T
        self.K = K
        self.steps = steps
        self.dt = T/steps
        self.t = 0

    def update_price(self):
        epsilon = np.random.normal()
        self.stock_price += self.stock_price * (self.r * self.dt + self.stock_sigma * epsilon * self.dt ** 0.5)

    def run(self):
        for step in range(self.steps):
            self.update_price()


        return self.stock_price - self.K if self.stock_price > self.K else 0
b = []

for _ in range(1000):
    a = Path(100, 0.06, 1, 99, 1000, 0.2)
    b.append(a.run())

print(np.mean(b))
print(np.std(b)/np.sqrt(len(b)))