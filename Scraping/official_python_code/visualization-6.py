from qiskit import QuantumCircuit
from qiskit.quantum_info import DensityMatrix
from qiskit.visualization import plot_state_city

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0,1)

# plot using a DensityMatrix
state = DensityMatrix(qc)
plot_state_city(state)