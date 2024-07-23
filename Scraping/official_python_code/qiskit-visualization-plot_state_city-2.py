# You can make the bars more transparent to better see the ones that are behind
# if they overlap.

import numpy as np
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_state_city
from qiskit import QuantumCircuit

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)


qc = QuantumCircuit(2)
qc.h([0, 1])
qc.cz(0,1)
qc.ry(np.pi/3, 0)
qc.rx(np.pi/5, 1)

state = Statevector(qc)
plot_state_city(state, alpha=0.6)