from qiskit.circuit import QuantumCircuit
from qiskit.quantum_info.operators import Operator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
def create_operator() -> QuantumCircuit:
    """ Create a Qiskit circuit with the following unitary [[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]], consisting of only single-qubit gates and CX gates, then transpile the circuit using pass manager with optimization level as 1.
    """
    qc = QuantumCircuit(2)
    qc.cx(0, 1)
    qc.cx(0, 1)
    qc.cx(0, 1)
    qc.cx(0, 1)
    qc.cx(0, 1)
    qc.cx(0, 1)
    qc.cx(0, 1)
    qc.cx(0, 1)
    qc.cx(0, 1)
    qc.cx(0, 1)
    qc.cx(0, 1)
    qc.cx(0, 1)
    qc.cx(0, 1)
    qc.cx(0, 1)
    qc.cx(0, 1)
    qc.cx(0, 1)
    qc.cx(0, 1)
    qc.cx(0, 1)
    qc.cx(0, 1)
    qc.cx(0, 1)
    qc.cx(0, 1)
    qc.cx(0, 1)
    qc.