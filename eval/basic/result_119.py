from qiskit.circuit.library import CDKMRippleCarryAdder
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator
def create_ripple_carry_adder_circuit(num_state_qubits: int, kind: str) -> QuantumCircuit:
    """ Create a QuantumCircuit with a CDKMRippleCarryAdder applied to the qubits.
    The kind of adder can be 'full', 'half', or 'fixed'.
    """
    # Create a QuantumCircuit with num_state_qubits qubits
    circuit = QuantumCircuit(num_state_qubits)

    # Apply the CDKMRippleCarryAdder to the qubits
    if kind == "full":
        circuit.append(CDKMRippleCarryAdder(num_state_qubits), circuit.qubits)
    elif kind == "half":
        circuit.append(CDKMRippleCarryAdder(num_state_qubits, half=True), circuit.qubits)
    elif kind == "fixed":
        circuit.append(CDKMRippleCarryAdder(num_state_qubits, fixed=True), circuit.qubits)

    return circuit

def create_ripple_carry_adder_operator(num_state_qubits: int, kind: str) -> Operator:
    """ Create an Operator with a CDKMRippleCarryAdder applied to the qubits.
    The kind of adder can be 'full', 'half', or 'fixed'.
    """
    # Create a QuantumCircuit with num_state_qubits qubits
    circuit = create_ripple_carry_adder_circuit(num