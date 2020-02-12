import numpy as np

class Stock:
	def __init__(self, starting_price, sigma, r, T, steps):
		self.price = starting_price
		self.sigma = sigma
		self.r = r
		self.end = T
		self.steps = steps
		self.dt = T/steps

	def step(self):
		epsilon = np.random.normal()
		self.price += self.price * (self.r * self.dt + self.sigma  * epsilon * self.dt**0.5)

	def run(self):
		for step in range(steps)


print(np.random.normal())