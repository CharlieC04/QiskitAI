from qiskit.dagcircuit import DAGCircuit
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit.converters import circuit_to_dag
def bell_dag() -> DAGCircuit:
    """ Construct a DAG circuit for a 3-qubit Quantum Circuit with the bell state applied on qubit 0 and 1. Finally return the DAG Circuit object.
    """
    qr = QuantumRegister(3)
    cr = ClassicalRegister(3)
    circuit = QuantumCircuit(qr, cr)
    circuit.h(qr[0])
    circuit.cx(qr[0], qr[1])
    circuit.measure(qr, cr)
    dag = circuit_to_dag(circuit)
    return dag
bell_dag()

from qiskit.dagcircuit import DAGCircuit
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit.converters import circuit_to_dag
def bell_dag() -> DAGCircuit:
    """ Construct a DAG circuit for a 3-qubit Quantum Circuit with the bell state applied on qubit 0 and 1. Finally return the DAG Circuit object.
    """
    qr = QuantumRegister(3)
    cr = ClassicalRegister(3)
    circuit = QuantumCircuit(qr, cr)
    circuit.h(qr[0])
    circuit.cx(qr[0], qr[1])
    circuit.measure(qr, cr)
    dag = circuit_to_dag(circuit)
    return dag
bell_dag()

from qis