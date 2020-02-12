import numpy as np
from scipy.stats import norm

class Tree:
	def __init__(self, depth, K, S0, r, sigma, T=1, american=False):
		self.depth = depth
		self.layers = []
		self.T = T
		self.dt = T / (depth - 1)
		self.u = np.exp(sigma * np.sqrt(dt))
		self.d = np.exp(-sigma * np.sqrt(dt))
		self.p = (np.exp(r * dt) - self.d) / (self.u - self.d)

		self.create(self.dt)
		self.assign_children()
		self.price_stocks(S0)
		self.price_options(K, r)

	def create(self, dt):
		for row in range(1, self.depth + 1):
			layer = []
			for i in range(row):
				layer.append(Node(row, i))
			self.layers.append(layer)

	def assign_children(self):
		for i in range(self.depth - 1):
			for j in range(len(self.layers[i])):
				self.layers[i][j].children = [self.layers[i+1][j], self.layers[i+1][j+1]]

	def price_stocks(self, S0):
		self.layers[0][0].stock_price = S0

		for layer in self.layers[:-1]:
			for node in layer:
				node.stock_pricer(self.u, self.d)

	def price_options(self, K, r):
		for layer in self.layers[::-1]:
			for node in layer:
				node.option_pricer(K, r, self.p, self.dt)
				node.analytical_pricer(K, r, sigma, self.dt, self.T, self.depth)
				if american:
					node.option_price = max(K - node.stock_price, node.option_price)
class Node:
	def __init__(self, layer, index):
		self.stock_price = 0
		self.option_price = 0
		self.analytical_price = 0
		self.layer = layer
		self.index = index
		self.children = []

	def __str__(self):
		return f"Layer: {self.layer}, #{self.index+1}, S: {self.stock_price}, f: {self.option_price}, analytic: {self.analytical_price}"

	def stock_pricer(self, u, d):
		if len(self.children) == 2:
			if self.children[0].stock_price == 0:
				self.children[0].stock_price = u * self.stock_price
			if self.children[1].stock_price == 0:
				self.children[1].stock_price = d * self.stock_price

	def option_pricer(self, K, r, p, dt):
		if len(self.children) == 2:
			up = self.children[0].option_price
			down = self.children[1].option_price
			self.option_price = (p * up + (1 - p) * down) * np.exp(-r * dt)
		else:
			self.option_price = max(self.stock_price - K, 0)

	def analytical_pricer(self, K, r, sigma, dt, T, depth):
		if self.layer == depth:
			self.analytical_price = max(self.stock_price - K, 0)
		else:
			t = (self.layer - 1) * dt
			d1 = 1/(sigma*np.sqrt(T-t)) * (np.log(self.stock_price/K) + (r+((sigma**2)/2))*(T-t))
			d2 = d1 - (sigma*np.sqrt(T-t))
			self.analytical_price = norm.cdf(d1)*self.stock_price - norm.cdf(d2)*K*np.exp(-r*(T-t))

	def hedge(self):
		if len(self.children) == 0:
			print("Hedging not possible for option at expiry date.")
		else:
			df = self.children[0].option_price - self.children[1].option_price
			ds = self.children[0].stock_price - self.children[1].stock_price
			if ds == 0:
				print("Stock prices have not yet been set.")
			elif df == 0:
				print("Hedging not possible as option has no value.")
			else:
				return (df / ds)

# Input variables
K = 50
S0 = 50
r = 0.10
sigma = 0.40
dt = 0.0833

tree = Tree(6, K, S0, r, sigma, 5/12)
for layer in tree.layers:
	for node in layer:
		print(node)
		print(f"Hedge parameter: {node.hedge()}")
