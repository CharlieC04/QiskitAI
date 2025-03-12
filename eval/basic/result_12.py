from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator
def get_unitary() -> Operator:
    """ Get unitary matrix for a phi plus bell circuit and return it.
    """
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.rz(0.5, 1)
    qc.cx(0, 1)
    qc.h(0)
    return Operator(qc)

get_unitary()