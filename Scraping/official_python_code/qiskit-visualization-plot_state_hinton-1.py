import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import DensityMatrix
from qiskit.visualization import plot_state_hinton

qc = QuantumCircuit(2)
qc.h([0, 1])
qc.cz(0,1)
qc.ry(np.pi/3 , 0)
qc.rx(np.pi/5, 1)

state = DensityMatrix(qc)
plot_state_hinton(state, title="New Hinton Plot")