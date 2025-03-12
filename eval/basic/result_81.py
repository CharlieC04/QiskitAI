from qiskit import QuantumCircuit
def convert_qasm_string_to_quantum_circuit() -> QuantumCircuit:
    """ Generate a QASM 2 string representing a Phi plus Bell state quantum circuit. Then, convert this QASM 2 string into a Quantum Circuit object and return the resulting circuit.
    """
    qasm_string = """
    OPENQASM 2.0;
    include "qelib1.inc";
    qreg q[2];
    creg c[2];
    h q[0];
    cx q[0], q[1];
    """
    return QuantumCircuit.from_qasm_str(qasm_string)

qc = convert_qasm_string_to_quantum_circuit()
qc.draw()