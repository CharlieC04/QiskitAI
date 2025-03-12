from qiskit import QuantumCircuit
from qiskit.quantum_info import CNOTDihedral
def initialize_cnot_dihedral() -> CNOTDihedral:
    """ Initialize a CNOTDihedral element from a QuantumCircuit consist of 2-qubits with cx gate on qubit 0 and 1 and t gate on qubit 0 and return.
    """
    qc = QuantumCircuit(2)
    qc.cx(0, 1)
    qc.t(0)
    return CNOTDihedral.from_circuit(qc)

initialize_cnot_dihedral()