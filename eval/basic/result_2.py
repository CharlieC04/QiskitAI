from qiskit.quantum_info import Statevector
from math import sqrt
def create_bell_statevector() -> Statevector:
    """ Return a phi+ Bell statevector.
    """
    return Statevector.from_label('00') + Statevector.from_label('11')

def create_bell_statevector_from_qubits(qubit_1: QuantumRegister, qubit_2: QuantumRegister) -> Statevector:
    """ Return a phi+ Bell statevector.
    """
    return Statevector.from_label('00', qubit_1, qubit_2) + Statevector.from_label('11', qubit_1, qubit_2)

def create_bell_statevector_from_qubits_with_control(control_qubit: QuantumRegister, qubit_1: QuantumRegister, qubit_2: QuantumRegister) -> Statevector:
    """ Return a phi+ Bell statevector.
    """
    return Statevector.from_label('00', control_qubit, qubit_1, qubit_2) + Statevector.from_label('11', control_qubit, qubit_1, qubit_2)

def create_bell_statevector_from_qubits_with_control_and_target(control