from qiskit import QuantumCircuit
def create_custom_controlled()-> QuantumCircuit:
    """ Create a custom 2-qubit gate with an X gate on qubit 0 and an H gate on qubit 1. Then, add two control qubits to this gate. Apply this controlled gate to a 4-qubit circuit, using qubits 0 and 3 as controls and qubits 1 and 2 as targets. Return the final circuit.
    """
    qc = QuantumCircuit(4)
    qc.x(0)
    qc.h(1)
    qc.append(qc.to_gate(), [0, 1])
    qc.cx(0, 2)
    qc.cx(0, 3)
    return qc

qc = create_custom_controlled()
qc.draw()