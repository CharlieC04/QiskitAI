from qiskit.synthesis import synth_clifford_full
from qiskit.quantum_info.random import random_clifford
def synthesize_clifford_circuit(n_qubits:int):
    """ Create a random clifford circuit using the random_clifford function for a given n qubits with seed 1234 and synthesize it using synth_clifford_full method and return.
    """
    clifford = random_clifford(n_qubits, seed=1234)
    circuit = synth_clifford_full(clifford)
    return circuit

circuit = synthesize_clifford_circuit(5)
circuit.draw()

from qiskit.synthesis import synth_clifford_full
from qiskit.quantum_info.random import random_clifford
def synthesize_clifford_circuit(n_qubits:int):
    """ Create a random clifford circuit using the random_clifford function for a given n qubits with seed 1234 and synthesize it using synth_clifford_full method and return.
    """
    clifford = random_clifford(n_qubits, seed=1234)
    circuit = synth_clifford_full(clifford)
    return circuit

circuit = synthesize_clifford_circuit(5)
circuit.draw()

from qiskit.synthesis import synth_clifford_full
from qiskit.quantum_info.random import