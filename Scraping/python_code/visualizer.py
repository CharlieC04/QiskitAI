from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, QISKitError
from qiskit import available_backends, execute, register, get_backend

# import state tomography functions
from qiskit.tools.visualization import plot_histogram, plot_state

# useful additional packages
import matplotlib.pyplot as plt
#%matplotlib inline
import numpy as np
from pprint import pprint
from scipy import linalg as la

def ghz_state(q, c, n):
    # Create a GHZ state
    qc = QuantumCircuit(q, c)
    qc.h(q[0])
    for i in range(n-1):
        qc.cx(q[i], q[i+1])
    return qc

def superposition_state(q, c):
    # Create a Superposition state
    qc = QuantumCircuit(q, c)
    qc.h(q)
    return qc

def overlap(state1, state2):
    return round(np.dot(state1.conj(), state2))

def expectation_value(state, Operator):
    return round(np.dot(state.conj(), np.dot(Operator, state)).real)

def state_2_rho(state):
    return np.outer(state, state.conj())

# Build the quantum cirucit. We are going to build two circuits a GHZ over 3 qubits and a
# superpositon over all 3 qubits

n = 3  # number of qubits
q = QuantumRegister(n)
c = ClassicalRegister(n)
'''
# quantum circuit to make a GHZ state
ghz = ghz_state(q, c, n)

# quantum circuit to make a superposition state
superposition = superposition_state(q, c)

measure_circuit = QuantumCircuit(q,c)
measure_circuit.measure(q, c)

# execute the quantum circuit
backend = 'local_qasm_simulator' # the device to run on
circuits = [ghz+measure_circuit, superposition+measure_circuit]
job = execute(circuits, backend=backend, shots=1000)
plot_histogram(job.result().get_counts(circuits[0]))
plot_histogram(job.result().get_counts(circuits[1]),15)
'''
qc = QuantumCircuit(q, c)
qc.h(q[1])

# execute the quantum circuit
job = execute(qc, backend='local_statevector_simulator')
state_superposition = job.result().get_statevector(qc)
#print(state_superposition)
#print(overlap(state_superposition, state_superposition))
rho_superposition = state_2_rho(state_superposition)
print(rho_superposition)
plot_state(rho_superposition, 'bloch') #'city', 'paulivec', 'qsphere', 'bloch'