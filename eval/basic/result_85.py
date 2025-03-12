from qiskit import QuantumCircuit
import qiskit.qasm2
def convert_quantum_circuit_to_qasm_string(circuit: QuantumCircuit) -> str:
    """ Given a QuantumCircuit, convert it into qasm2 string and return it.
    """
    return qiskit.qasm2.qasm2_str(circuit)