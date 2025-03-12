from qiskit import QuantumCircuit
from qiskit.quantum_info import CNOTDihedral
def compose_cnot_dihedral() -> CNOTDihedral:
    """ Create two Quantum Circuits of 2 qubits. First quantum circuit should have a cx gate on qubits 0 and 1 and a T gate on qubit 0. The second one is the same but with an additional X gate on qubit 1. Convert the two quantum circuits into CNOTDihedral elements and return the composed circuit.
    """
    qc1 = QuantumCircuit(2)
    qc1.cx(0, 1)
    qc1.t(0)
    qc2 = QuantumCircuit(2)
    qc2.cx(0, 1)
    qc2.x(1)
    return CNOTDihedral(qc1), CNOTDihedral(qc2)

compose_cnot_dihedral()