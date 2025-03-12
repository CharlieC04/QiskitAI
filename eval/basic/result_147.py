from qiskit import QuantumCircuit
from qiskit.circuit.library import YGate
def mcy(qc: QuantumCircuit) -> QuantumCircuit:
    """ Add a multi-controlled-Y operation to qubit 4, controlled by qubits 0-3.
    """
    qc.append(YGate(), [4] + list(range(0, 4)))
    return qc

qc = QuantumCircuit(5)
qc.h(0)
qc.cx(0, 1)
qc.cx(1, 2)
qc.cx(2, 3)
qc.cx(3, 4)
qc.append(mcy(qc), [4] + list(range(0, 4)))
qc.draw()

from qiskit import QuantumCircuit
from qiskit.circuit.library import YGate
def mcy(qc: QuantumCircuit) -> QuantumCircuit:
    """ Add a multi-controlled-Y operation to qubit 4, controlled by qubits 0-3.
    """
    qc.append(YGate(), [4] + list(range(0, 4)))
    return qc

qc = QuantumCircuit(5)
qc.h(0)
qc.cx(0, 1)
qc.cx(1, 2)
qc.cx(2, 3)
qc.cx(3,