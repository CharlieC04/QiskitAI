from numpy import float64
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Estimator
from qiskit.quantum_info import SparsePauliOp
def estimator_qiskit() -> float64:
    """ Run a Bell circuit on Qiskit Estimator and return expectation values for the bases II, XX, YY, ZZ.
    """
    # Create a Bell circuit
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)

    # Create a SparsePauliOp from the circuit
    pauli_op = SparsePauliOp.from_circuit(qc)

    # Create an Estimator instance
    estimator = Estimator()

    # Run the estimator on the circuit
    result = estimator.run(pauli_op).result()

    # Get the expectation values for the bases II, XX, YY, ZZ
    ii_exp = result.values[0]
    xx_exp = result.values[1]
    yy_exp = result.values[2]
    zz_exp = result.values[3]

    # Return the expectation values
    return ii_exp, xx_exp, yy_exp, zz_exp

def estimator_qiskit_aer() -> float64:
    """ Run a Bell circuit on Qiskit Aer Simulator and return expectation values for the bases II, XX, YY, ZZ.
    """
    # Create a Bell circuit
    qc = QuantumCircuit(2)
    qc.h(0)