from qiskit import QuantumCircuit
import qiskit.qasm3
def convert_quantum_circuit_to_qasm_string(circuit: QuantumCircuit) -> str:
    """ Given a Quantum Circuit as the argument, convert it into qasm3 string and return it.
    """
    qasm_string = qiskit.qasm3.dump(circuit)
    return qasm_string