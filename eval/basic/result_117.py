from qiskit.synthesis import TwoQubitBasisDecomposer
from qiskit.quantum_info import Operator, random_unitary
from qiskit.circuit.library import CXGate
from qiskit import QuantumCircuit
import numpy as np
def decompose_unitary(unitary: Operator) -> QuantumCircuit:
    """ Decompose a 4x4 unitary using the TwoQubitBasisDecomposer with CXGate as the basis gate.
    Return the resulting QuantumCircuit.
    """
    # YOUR CODE HERE
    basis_gates = [CXGate()]
    decomposer = TwoQubitBasisDecomposer(basis_gates)
    return decomposer.decompose(unitary)

unitary = random_unitary(4)
qc = decompose_unitary(unitary)
qc.draw('mpl')

# +
from qiskit.synthesis import TwoQubitBasisDecomposer
from qiskit.quantum_info import Operator, random_unitary
from qiskit.circuit.library import CXGate
from qiskit import QuantumCircuit
import numpy as np
def decompose_unitary(unitary: Operator) -> QuantumCircuit:
    """ Decompose a 4x4 unitary using the TwoQubitBasisDecomposer with CXGate as the basis gate.
    Return the resulting QuantumCircuit.
    """
    # YOUR CODE HERE
    basis_gates = [CXGate()]
    decomposer = TwoQubitBasisDecomposer(basis_gates)
    return decomposer.decompose(unitary)

unitary = random_unitary(4)
qc = decompose_unitary(unitary)
