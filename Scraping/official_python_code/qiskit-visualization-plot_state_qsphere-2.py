# You can show the phase of each state and use
# degrees instead of radians

from qiskit.quantum_info import DensityMatrix
import numpy as np
from qiskit import QuantumCircuit
from qiskit.visualization import plot_state_qsphere

qc = QuantumCircuit(2)
qc.h([0, 1])
qc.cz(0,1)
qc.ry(np.pi/3, 0)
qc.rx(np.pi/5, 1)
qc.z(1)

matrix = DensityMatrix(qc)
plot_state_qsphere(matrix,
     show_state_phases = True, use_degrees = True)