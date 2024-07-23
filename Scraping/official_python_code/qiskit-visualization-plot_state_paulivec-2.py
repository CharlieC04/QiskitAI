# If you introduce a list with less colors than bars, the color of the bars will
# alternate following the sequence from the list.

import numpy as np
from qiskit.quantum_info import DensityMatrix
from qiskit import QuantumCircuit
from qiskit.visualization import plot_state_paulivec

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)

qc = QuantumCircuit(2)
qc.h([0, 1])
qc.cz(0, 1)
qc.ry(np.pi/3, 0)
qc.rx(np.pi/5, 1)

matrix = DensityMatrix(qc)
plot_state_paulivec(matrix, color=['crimson', 'midnightblue', 'seagreen'])