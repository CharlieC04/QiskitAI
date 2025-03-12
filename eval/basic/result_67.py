from qiskit import QuantumCircuit
from numpy import pi
def chsh_circuit(alice: int, bob: int)->QuantumCircuit:
    """ Design a CHSH circuit that takes bits of Alice and Bob as input and return the Quantum Circuit after measuring.
    """
    qc = QuantumCircuit(2)
    if alice == 0:
        qc.x(0)
    if bob == 0:
        qc.x(1)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    return qc

qc = chsh_circuit(0, 0)
qc.draw()

from qiskit import Aer, execute
backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend, shots=1000)
result = job.result()
counts = result.get_counts()
print(counts)

qc = chsh_circuit(0, 1)
qc.draw()

job = execute(qc, backend, shots=1000)
result = job.result()
counts = result.get_counts()
print(counts)

qc = chsh_circuit(1, 0)
qc.draw()

job = execute(qc, backend, shots=1000)
result = job.result()