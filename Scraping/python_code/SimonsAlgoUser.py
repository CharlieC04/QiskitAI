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
b = input("input the bitstring key")

n = len(b)

#this is because we need double bits to act as both registers
simon_circuit = QuantumCircuit(n*2, n)

# Apply Hadamard gates before querying the oracle
simon_circuit.h(range(n))    
    
# Apply barrier for visual separation
simon_circuit.barrier()
arr = []

counter = 0

while counter < n*2:
    arr.append(counter)
    counter += 1

print (arr)
#append the black box to the circuit
simon_circuit.append(simon_oracle(b), arr)

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