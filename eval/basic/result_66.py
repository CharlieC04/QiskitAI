from qiskit import QuantumCircuit
from numpy import arccos, sqrt
def w_state()->QuantumCircuit:
    """ Generate a Quantum Circuit for a W state and measure it.
    """
    qc = QuantumCircuit(3)
    qc.h(0)
    qc.cx(0,1)
    qc.cx(1,2)
    qc.measure_all()
    return qc

qc = w_state()
qc.draw()

from qiskit import Aer, execute
backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend, shots=1000)
result = job.result()
counts = result.get_counts(qc)
print(counts)

from qiskit.visualization import plot_histogram
plot_histogram(counts)

qc = w_state()
qc.measure_all()
qc.draw()

from qiskit import Aer, execute
backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend, shots=1000)
result = job.result()
counts = result.get_counts(qc)
print(counts)

plot_histogram(counts)

qc = w_state()
qc.measure_all