from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
def get_statevector(circuit: QuantumCircuit) -> Statevector:
    """ Return the statevector from a circuit.
    """
    return Statevector.from_instruction(circuit)
