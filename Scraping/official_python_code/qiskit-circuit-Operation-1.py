from qiskit import QuantumCircuit
from qiskit.quantum_info import Clifford, random_clifford

qc = QuantumCircuit(3)
cliff = random_clifford(2)
qc.append(cliff, [0, 1])
qc.ccx(0, 1, 2)
qc.draw('mpl')