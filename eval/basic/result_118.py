from qiskit import QuantumCircuit
from qiskit.circuit.library import C3SXGate
def create_c3sx_circuit() -> QuantumCircuit:
    """ Create a QuantumCircuit with a C3SXGate applied to the first four qubits.
    """
    circuit = QuantumCircuit(4)
    circuit.append(C3SXGate(), [0, 1, 2, 3])
    return circuit

circuit = create_c3sx_circuit()
circuit.draw()