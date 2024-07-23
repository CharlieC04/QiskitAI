%matplotlib inline
from qiskit import (
    ClassicalRegister,
    QuantumRegister,
    QuantumCircuit,
    execute,
    IBMQ
)

import matplotlib.pyplot as plt

#provider = IBMQ.load_account()
backend = provider.get_backend('ibmq_qasm_simulator') # Simulated quantum computer

q = QuantumRegister(1)   # Only 1 qubit
c = ClassicalRegister(1) # Only 1 qubit
circuit = QuantumCircuit(q, c)
circuit.h(q[0]) # Hadamard Gate
#circuit.h(q[1])  ## Second Qubit
#circuit.h(q[2])  ## Third Qubit ...
circuit.measure(q, c)
print(circuit)

job = execute(circuit, backend=backend, shots=1000)  # Number of attempts = 1000 attemps - The more attempts there are, the more equal the probabilities are
result = job.result()
counts = result.get_counts(circuit)
print(counts)
plt.bar(counts.keys(), counts.values(), 1, color='b')
