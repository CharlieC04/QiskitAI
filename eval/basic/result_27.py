from qiskit.dagcircuit import DAGCircuit
from qiskit.converters import circuit_to_dag
from qiskit.circuit.library import HGate
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
def apply_op_back() -> DAGCircuit:
    """ Generate a DAG circuit for 3-qubit Quantum Circuit which consists of H gate on qubit 0 and CX gate on qubit 0 and 1. After converting the circuit to DAG, apply a Hadamard operation to the back of qubit 0 and return the DAGCircuit.
    """
    qr = QuantumRegister(3)
    cr = ClassicalRegister(3)
    circuit = QuantumCircuit(qr, cr)
    circuit.h(qr[0])
    circuit.cx(qr[0], qr[1])
    dag = circuit_to_dag(circuit)
    dag.apply_operation_back(HGate(), [qr[0]])
    return dag
apply_op_back()