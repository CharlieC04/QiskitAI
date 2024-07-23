from dj import DeutschJozsa
import dj
import time
import sys
from random import seed
from random import randint
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from qiskit import *


def main():
	
	djObject = DeutschJozsa()

	# constants
	QUBIT_RANGE = 65
	ITERATIONS = 10


	worked = np.zeros(shape=(QUBIT_RANGE, ITERATIONS))
	timing = np.zeros(shape=(QUBIT_RANGE, ITERATIONS))

	print('Testing out Deutsch-Jozsa alorithm...')

	seed(3)
	for n in range(0,QUBIT_RANGE):
		print(f'Trying {n+2}-qubit machine...')
		for j in range(ITERATIONS):
			print(f'Iteration {j+1}...')

			# randomly decide f
			const_val = randint(0,1)
			def f_constant(_):
				return const_val
			def f_balanced(x):
				return x%2

			constant = randint(0,1)
			f = f_constant if constant else f_balanced
			print(constant)
			oracle = dj.dj_oracle(constant, n+2)
			start = time.perf_counter()
			result = djObject.run(f,oracle, n+2)
			end = time.perf_counter()

			# print('worked' if result == constant else 'failed')
			timing[n][j] = (end - start)

	qubit_values = []
	for i in range(QUBIT_RANGE):
		qubit_values += [i+2]

	average_runtimes = []
	for i in range(QUBIT_RANGE):
		average_runtimes += [np.mean(timing[i])]

	plt.plot(qubit_values, average_runtimes)
	plt.ylabel('Runtime (s)')
	plt.xlabel('Number of Qubits')
	plt.xticks(qubit_values)
	plt.title('Quantum Simulation Scaling for Deutsch-Jozsa Algorithm')
	plt.show()

if __name__ == "__main__":
	main()