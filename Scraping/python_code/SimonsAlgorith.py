# importing Qiskit
from qiskit import Aer
from qiskit.providers.aer import AerSimulator
from qiskit.providers.ibmq import least_busy
from qiskit import *
# import basic plot tools
from qiskit.visualization import plot_histogram
from qiskit_textbook.tools import simon_oracle
from IPython.display import display


# This will be our bitstring key
b = '110'

n = len(b)

#this is because we need double bits to act as both registers
simon_circuit = QuantumCircuit(n*2, n)

# Apply Hadamard gates before querying the oracle
simon_circuit.h(range(n))    
    
# Apply barrier for visual separation
simon_circuit.barrier()

#append the black box to the circuit
simon_circuit.append(simon_oracle(b), [0,1,2,3,4,5])

# Apply barrier for visual separation
simon_circuit.barrier()

# Apply Hadamard gates to the input register
simon_circuit.h(range(n))

# Measure qubits
simon_circuit.measure(range(n), range(n))
display(simon_circuit.draw())

# use local simulator
sim = Aer.get_backend('qasm_simulator')
result = execute(simon_circuit, backend = sim, shots = 1024).result()
counts = result.get_counts()
print(counts)
display(plot_histogram(counts))