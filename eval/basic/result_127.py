from qiskit.circuit.random import random_circuit
from qiskit import QuantumCircuit
def random_circuit_depth():
    """ Using qiskit's random_circuit function, generate a circuit with 4 qubits and a depth of 3 that measures all qubits at the end. Use the seed value 17 and return the generated circuit.
    """
    circuit = random_circuit(4, 3, seed=17)
    circuit.measure_all()
    return circuit

circuit = random_circuit_depth()
circuit.draw()

from qiskit.circuit.library import RealAmplitudes
from qiskit.circuit.library import EfficientSU2
from qiskit.circuit.library import TwoLocal
from qiskit.circuit.library import ZZFeatureMap
from qiskit.circuit.library import PauliFeatureMap
from qiskit.circuit.library import ZFeatureMap
from qiskit.circuit.library import PauliFeatureMap
from qiskit.circuit.library import ZZFeatureMap
from qiskit.circuit.library import PauliFeatureMap
from qiskit.circuit.library import ZFeatureMap
from qiskit.circuit.library import PauliFeatureMap
from qiskit.circuit.library import ZZFeatureMap
from qiskit.circuit.library import PauliFeatureMap
from qiskit.circuit.library import ZFeatureMap
from qiskit.circuit.library import PauliFeatureMap
from qiskit.circuit.