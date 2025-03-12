from qiskit import QuantumCircuit
from qiskit.circuit import Gate
def count_gates(circuit: QuantumCircuit) -> int:
    """ Return the total number of unitary gates in the circuit.
    """
    return sum(1 for gate in circuit.data if isinstance(gate, Gate))

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.cx(0, 1)
qc.cx(0, 1)
qc.cx(0, 1)
qc.cx(0, 1)
qc.cx(0, 1)
qc.cx(0, 1)
qc.cx(0, 1)
qc.cx(0, 1)
qc.cx(0, 1)
qc.cx(0, 1)
qc.cx(0, 1)
qc.cx(0, 1)
qc.cx(0, 1)
qc.cx(0, 1)
qc.cx(0, 1)
qc.cx(0, 1)
qc.cx(0, 1)
qc.cx(0, 1)
qc.cx(0, 1)
qc.cx(0, 1)
qc.cx(0, 1)
