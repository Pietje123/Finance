import numpy as np
from scipy.stats import norm


class Tree:
    def __init__(self, depth, K, S0, r, sigma, T=1, call=True, american=False):
        self.depth = depth
        self.layers = []
        self.T = T
        self.sigma = sigma
        self.dt = T / (depth - 1)
        self.u = np.exp(self.sigma * np.sqrt(self.dt))
        self.d = np.exp(-self.sigma * np.sqrt(self.dt))
        self.p = (np.exp(r * self.dt) - self.d) / (self.u - self.d)

        self.create(self.dt)
        self.assign_children()
        self.price_stocks(S0)
        self.price_options(K, r, call, american)

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

    def price_options(self, K, r, call, american):
        for layer in self.layers[::-1]:
            for node in layer:
                node.option_pricer(K, r, self.p, self.dt, call)
                node.analytical_pricer(K, r, self.sigma, self.dt, self.T, self.depth, call)
                if american:
                    if call:
                        print(node.option_price - max(node.stock_price - K, node.option_price))
                        node.option_price = max(node.stock_price - K, node.option_price)
                    else:
                        print(node.option_price - max(K - node.stock_price, node.option_price))
                        node.option_price = max(K -node.stock_price, node.option_price)

    def root_option_diff(self):
        return self.layers[0][0].option_price - self.layers[0][0].analytical_price

    def root_hedge_diff(self):
        pass


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

    def option_pricer(self, K, r, p, dt, call):
        if len(self.children) == 2:
            up = self.children[0].option_price
            down = self.children[1].option_price
            self.option_price = (p * up + (1 - p) * down) * np.exp(-r * dt)
        else:
            if call:
                self.option_price = max(self.stock_price - K, 0)
            else:
                self.option_price = max(K - self.stock_price, 0)

    def analytical_pricer(self, K, r, sigma, dt, T, depth, call):
        if self.layer == depth:
            if call:
                self.analytical_price = max(self.stock_price - K, 0)
            else:
                self.analytical_price = max(K - self.stock_price, 0)
        else:
            t = (self.layer - 1) * dt
            d1 = 1/(sigma*np.sqrt(T-t)) * (np.log(self.stock_price/K) + (r+((sigma**2)/2))*(T-t))
            d2 = d1 - (sigma*np.sqrt(T-t))
            if call:
                self.analytical_price = norm.cdf(d1)*self.stock_price - norm.cdf(d2)*K*np.exp(-r*(T-t))
            else:
                self.analytical_price = -norm.cdf(-d1)*self.stock_price + norm.cdf(-d2)*K*np.exp(-r*(T-t))

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