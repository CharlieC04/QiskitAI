#initialization
import matplotlib.pyplot as plt
import numpy as np
import math

# importing Qiskit
from qiskit import Aer, transpile, execute
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit.providers.ibmq import least_busy
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler
from qiskit.primitives import Estimator
from qiskit.circuit import ParameterVector
from qiskit_ibm_provider import IBMProvider
from qiskit_ibm_provider import least_busy
import qiskit_ibm_provider

provider = qiskit_ibm_provider.IBMProvider()

# -->  simulator backend = provider.get_backend('ibmq_qasm_simulator')


n = 2
grover_circuit = QuantumCircuit(n)

def initialize_s(qc, qubits):
    """Apply a H-gate to 'qubits' in qc"""
    for q in qubits:
        qc.h(q)
    return qc

grover_circuit = initialize_s(grover_circuit, [0,1])
print(grover_circuit)

grover_circuit.cz(0,1) # Oracle
print("Oracle :",end='\n')
print(grover_circuit)

# Diffusion operator (U_s)
grover_circuit.h([0,1])
grover_circuit.z([0,1])
grover_circuit.cz(0,1)
grover_circuit.h([0,1])
print("Oracle + Diffusion :",end='\n')
print(grover_circuit)

sv_sim = Aer.get_backend('statevector_simulator')
result = sv_sim.run(grover_circuit).result()
statevec = result.get_statevector()
grover_circuit.measure_all()

# display current supported backends
print("IBMQ Q system ready with almost 5 qubits",end='\n')
print(provider.backends(min_num_qubits=5, simulator=False, operational=True))
small_devices = provider.backends(min_num_qubits=5, simulator=False, operational=True)
backend = least_busy(small_devices)
print("BACKEND : ",backend)

#running the job
job_exp = execute(grover_circuit, backend, shots=2048)
result_exp = job_exp.result()

# Show the results
print('Counts: ', result_exp.get_counts(grover_circuit))


