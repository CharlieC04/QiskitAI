from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT


def qft_no_swaps(num_qubits: int) -> QuantumCircuit:
    """ Return an inverse quantum Fourier transform circuit without the swap gates.
    """
    qc = QFT(num_qubits)
    qc.inverse()
    return qc


def qft_with_swaps(num_qubits: int) -> QuantumCircuit:
    """ Return an inverse quantum Fourier transform circuit with the swap gates.
    """
    qc = QFT(num_qubits)
    qc.inverse()
    qc.swap(0, num_qubits - 1)
    return qc

