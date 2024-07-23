import numpy as np

from qiskit import BasicAer
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, execute
from qiskit.providers.ibmq import least_busy
from qiskit.visualization import plot_histogram
from qiskit import IBMQ, assemble, transpile
from qiskit.tools.monitor import job_monitor
from qiskit.tools.monitor import job_monitor

import argparse, sys
import time

provider = IBMQ.load_account()
parser = argparse.ArgumentParser()
parser.add_argument('--s', help = 'Enter the secret string.')


class Bernstein_Vazirani(object):
	def __init__(self, n, s):
		self.n = n
		self.s = s

	def _run_bv(self):
		bv_circuit = QuantumCircuit(self.n+1,self.n)

		bv_circuit.h(self.n)
		bv_circuit.barrier()
		bv_circuit.z(self.n) 
		bv_circuit.barrier()

		for i in range(self.n):
		    bv_circuit.h(i)
		    
		bv_circuit.barrier()
		s = self.s[::-1]
		for q in range(self.n):
		    if s[q] == '0':
		        bv_circuit.i(q)
		    else:
		    	bv_circuit.cx(q, self.n)
		bv_circuit.barrier()
		for i in range(self.n):
		    bv_circuit.h(i)
		bv_circuit.barrier()
		for i in range(self.n):
			bv_circuit.measure(i, i)

		backend = least_busy(provider.backends(filters=lambda x: x.configuration().n_qubits >= len(self.qubits) and not x.configuration().simulator and x.status().operational==True))
		print("least busy backend: ", backend)
		shots = 8000
		job = execute(bv_circuit, backend=backend, shots=shots, optimization_level=3)
		job_monitor(job, interval = 2)

		try: 
			result = job.result()
		except:
			print(job.error_message())
			return -1, -1
		answer = result.get_counts(bv_circuit)
		print(answer)

		fi = plot_histogram(answer)
		fi.savefig(fname = "bv_results4_8000.png")
        
		print("--%s seconds--" % result.time_taken)
		

if __name__ == '__main__':
	start_time = time.time()
	args = parser.parse_args()
	s = args.s
	for i in s:
		if i != '0' and i != '1':
			raise AssertionError("s must be a bitstring")
	n = len(s)
	bv = Bernstein_Vazirani(n, s)
	bv._run_bv()