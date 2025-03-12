from qiskit.circuit.library import QFT
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator
def qft_inverse(n: int):
    """ Return the inverse qft circuit for n qubits.
    """
    qc = QuantumCircuit(n)
    qc.append(QFT(n, inverse=True), range(n))
    return qc

def qft_dagger(n: int):
    """ Return the dagger of the qft circuit for n qubits.
    """
    qc = QuantumCircuit(n)
    qc.append(QFT(n, inverse=True), range(n))
    return qc.to_gate()

def qft_dagger_matrix(n: int):
    """ Return the dagger of the qft matrix for n qubits.
    """
    qc = QuantumCircuit(n)
    qc.append(QFT(n, inverse=True), range(n))
    return Operator(qc).data

def qft_matrix(n: int):
    """ Return the qft matrix for n qubits.
    """
    qc = QuantumCircuit(n)
    qc.append(QFT(n), range(n))
    return Operator(qc).data

def qft_dagger_operator(n: int):
    """ Return the dagger of the qft operator for n qubits