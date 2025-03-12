from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler
from numpy import pi
def zeno_elitzur_vaidman_bomb_tester(bomb_live: bool) -> (float, float, float):
    """ Design a Zeno Elitzur Vaidman Bomb Tester circuit which takes the boolean if the bomb is live and outputs the percentage of successful live bomb predictions, dud bomb predictions and bombs that detonated. Use 25 cycles to increase the efficiency of the circuit.
    """
    # Create a Quantum Circuit with 2 qubits and 2 classical bits
    qc = QuantumCircuit(2, 2)

    # Apply Hadamard gates to the first qubit
    qc.h(0)

    # Apply CNOT gates to the first and second qubits
    qc.cx(0, 1)

    # Apply Hadamard gates to the first qubit
    qc.h(0)

    # Apply CNOT gates to the first and second qubits
    qc.cx(0, 1)

    # Apply Hadamard gates to the first qubit
    qc.h(0)

    # Apply CNOT gates to the first and second qubits
    qc.cx(0, 1)

    # Apply Hadamard gates to the first qubit
    qc.h(0)

    # Apply CNOT gates to the first and second qubits
    qc.cx(0, 1)

    # Apply Hadamard gates to the first qubit
    qc.h(0)

    # Apply CNOT gates to the first and second qubits
    qc.cx(