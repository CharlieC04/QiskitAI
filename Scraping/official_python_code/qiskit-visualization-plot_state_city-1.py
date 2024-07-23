# You can choose different colors for the real and imaginary parts of the density matrix.

from qiskit import QuantumCircuit
from qiskit.quantum_info import DensityMatrix
from qiskit.visualization import plot_state_city

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)

state = DensityMatrix(qc)
plot_state_city(state, color=['midnightblue', 'crimson'], title="New State City")