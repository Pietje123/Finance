import numpy as np

# Input variables
K = 52
S0 = 50
r = 0.06
sigma = 0.20
dt = 0.25

# Model Parameters
u = 1.2
# np.exp(sigma * np.sqrt(dt))
d = 0.8
# np.exp(-sigma * np.sqrt(dt))

class Tree:
	def __init__(self, depth):
		self.depth = depth
		self.layers = []
		self.create()
		self.assign_children()

	def create(self):
		for row in range(1, self.depth + 1):
			layer = []
			for i in range(row):
				layer.append(Node(row))
			self.layers.append(layer)

	def assign_children(self):
		for i in range(self.depth - 1):
			for j in range(len(self.layers[i])):
				self.layers[i][j].children = [self.layers[i+1][j], self.layers[i+1][j+1]]

class Node:
	def __init__(self, layer):
		self.stock_price = 0
		self.option_price = 0
		self.layer = layer
		self.children = []

	def option_pricer(self, r):
		up = self.children[0].option_price
		down = self.children[1].option_price
		p = (np.exp(r * dt) - d) / (u - d)
		print(up, down, p)


		self.option_price = (p * up + (1 - p) * down) * np.exp(-r * dt)

tree = Tree(4)
tree.create()
tree.assign_children()

print(tree.layers)
print(tree.layers[0][0].children)
