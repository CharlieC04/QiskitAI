from qiskit import QuantumCircuit
from qiskit.circuit.library.standard_gates.equivalence_library import ( StandardEquivalenceLibrary as std_eqlib, )
from qiskit.transpiler.passes import BasisTranslator
from qiskit.transpiler import PassManager
import numpy as np
def unroll_circuit(circuit: QuantumCircuit) -> QuantumCircuit:
    """ Unroll circuit for the gateset: CX, ID, RZ, SX, X, U.
    """
    eqlib = std_eqlib()
    basis_translator = BasisTranslator(eqlib)
    pm = PassManager(basis_translator)
    return pm.run(circuit)

def get_unitary(circuit: QuantumCircuit) -> np.ndarray:
    """ Get unitary matrix of a circuit.
    """
    return unroll_circuit(circuit).unitary()

def get_unitary_from_qasm(qasm: str) -> np.ndarray:
    """ Get unitary matrix from qasm string.
    """
    circuit = QuantumCircuit.from_qasm_str(qasm)
    return get_unitary(circuit)

def get_unitary_from_qasm_file(qasm_file: str) -> np.ndarray:
    """ Get unitary matrix from qasm file.
    """
    with open(qasm_file, 'r') as f:
        qasm = f.read()
    return get_unitary_from_qasm(qasm)