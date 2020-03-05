import matplotlib.pyplot as plt
from montecarlo import Path
import multiprocessing as mp
import numpy as np
import os 
import json

plt.rcParams['figure.dpi'] = 150
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelsize'] = 14
cpus = mp.cpu_count()

def run_stock_steps(steps):
	return Path(starting_price=100, r=0.06, T=1, K=99, steps=steps, stock_sigma=0.2).run()

def run_stock_K(K):
	return Path(starting_price=100, r=0.06, T=1, K=K, steps=10000, stock_sigma=0.2).run()

def run_stock_sigma(sigma):
	return Path(starting_price=100, r=0.06, T=1, K=99, steps=10000, stock_sigma=sigma).run()


if not os.path.isdir('results'):
	os.mkdir('results')
	with open('results/steps.txt', 'w') as f:
		dummy = json.dumps({})
		f.write(dummy)
	with open('results/K.txt', 'w') as f:
		dummy = json.dumps({})
		f.write(dummy)
	with open('results/sigma.txt', 'w') as f:
		dummy = json.dumps({})
		f.write(dummy)

def read_file(file):
	with open(file) as f:
		data = f.readline()
	return json.loads(data)

def save_data(file, data):
	with open(file, 'w') as f:
		data = json.dumps(data)
		f.write(data)

def run_steps(times, steps):
	file = 'results/steps.txt'
	data = read_file(file)
	step_results = []

	for step in steps:
		if not str(step) in data:
			data = {str(i) : [] for i in steps}

	pool = mp.Pool(cpus)

	for _ in range(times):
		result = pool.map(run_stock_steps, steps)
		step_results.append(result)
	pool.close()
	zipped = list(zip(*step_results))
	for i in range(len(steps)):
		data[str(steps[i])].extend(zipped[i])
	save_data(file, data)




if __name__ == "__main__":
	steps = np.logspace(5,18, num=14, base=2, dtype=int)
	i = 0
	while 1e4 > i:
		print(int(1e4 - i))
		i+=1
		run_steps(1, steps)