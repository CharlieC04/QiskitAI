from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime.fake_provider import FakeHanoi

import sys

def example(n_qubits):
    return QuantumCircuit(n_qubits)

def generated(n_qubits):
    return QuantumCircuit(n_qubits)

ex_cirq = example(3)
gen_cirq = generated(3)

backend = FakeHanoi()

ex_transpile = transpile(ex_cirq, backend)
ex_job = backend.run(ex_transpile, shots=1024)
ex_result = ex_job.results().get_counts()

gen_transpile = transpile(gen_cirq, backend)
gen_job = backend.run(gen_transpile, shots=1024)
gen_result = gen_job.results().get_counts()

print(ex_results, gen_results)

epsilon = 0.1
for key in ex_result.keys():
    if abs(ex_result[key] - gen_result[key]) > epsilon:
        print("Fail")
        sys.exit(0)

print("Pass")
