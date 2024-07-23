import numpy as np
from qiskit import BasicAer
from qiskit.providers.ibmq import least_busy
from qiskit import QuantumCircuit, execute
from qiskit.visualization import plot_histogram
from qiskit import IBMQ, assemble, transpile
from qiskit.tools.monitor import job_monitor

import argparse, sys
import time

provider = IBMQ.load_account()

parser = argparse.ArgumentParser()
parser.add_argument('--bits', help = 'Enter the number of bits you want to run with.')
parser.add_argument('--algo', help = 'Enter either "constant" or "balanced".')


class Deutsch_Jozsa(object):
    def __init__(self, n, algo):
        self.n = n
        self.algo = algo

    #change to self
    def _dj_oracle(self):
        oracle_qc = QuantumCircuit(self.n+1)
        
        if self.algo == "balanced":
            b = np.random.randint(1,2**self.n)
            b_str = format(b, '0'+str(self.n)+'b')
            for qubit in range(len(b_str)):
                if b_str[qubit] == '1':
                    oracle_qc.x(qubit)
            for qubit in range(self.n):
                oracle_qc.cx(qubit, self.n)
            for qubit in range(len(b_str)):
                if b_str[qubit] == '1':
                    oracle_qc.x(qubit)

        if self.algo == "constant":
            output = np.random.randint(2)
            if output == 1:
                oracle_qc.x(self.n)
        
        return oracle_qc.to_gate()

    def _dj_algorithm(self, oracle):
        dj_circuit = QuantumCircuit(self.n+1, self.n)
        dj_circuit.x(self.n)
        dj_circuit.barrier()
        dj_circuit.h(self.n)
        dj_circuit.barrier()
        
        for qubit in range(self.n):
            dj_circuit.h(qubit)
        dj_circuit.barrier()
        dj_circuit.append(oracle, range(n+1))
        for qubit in range(self.n):
            dj_circuit.h(qubit)
        dj_circuit.barrier()
        for i in range(self.n):
            dj_circuit.measure(i, i)

    	
        backend = least_busy(provider.backends(filters=lambda x: x.configuration().n_qubits >= len(self.qubits) and not x.configuration().simulator and x.status().operational==True))
        print("least busy backend: ", backend)
        shots = 8000
        job = execute(dj_circuit, backend=backend, shots=shots, optimization_level=3)
        job_monitor(job, interval = 2)

        try: 
            result = job.result()
        except:
            print(job.error_message())
            return -1, -1
        answer = result.get_counts(dj_circuit)
        print(answer)

        fi = plot_histogram(answer)
        fi.savefig(fname = "dj_results5_8000.png")
        
        #fig = dj_circuit.draw(output = "mpl")
        #fig.savefig(fname = "dj6.png")
        print("--%s seconds--" % result.time_taken)

if __name__ == '__main__':
    start_time = time.time()
    args = parser.parse_args()
    n = int((args.bits))

    if n < 1:
        raise AssertionError("n must be a number of bits greater than 0")
    if args.algo != ('constant') and args.algo != ('balanced'):
        raise AssertionError("algo must be either balanced or constant")

    dj = Deutsch_Jozsa(n, args.algo)
    oracle_gate = dj._dj_oracle()
    dj_circuit = dj._dj_algorithm(oracle_gate)

	