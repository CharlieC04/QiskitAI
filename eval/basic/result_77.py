import math
from qiskit import QuantumCircuit
def circuit_from_probability_dist(probability_dist: dict[int, float]) -> QuantumCircuit:
    """ Given a distribution as a dictionary of the form { measurement: probability }, return a quantum circuit that produces that distribution.
    """
    circuit = QuantumCircuit(len(probability_dist))
    for measurement, probability in probability_dist.items():
        circuit.measure(measurement, measurement)
    return circuit

def probability_dist_from_circuit(circuit: QuantumCircuit) -> dict[int, float]:
    """ Given a quantum circuit, return a distribution as a dictionary of the form { measurement: probability }.
    """
    probability_dist = {}
    for measurement in range(circuit.num_qubits):
        probability_dist[measurement] = circuit.measurements[measurement].count / circuit.num_shots
    return probability_dist

def generate_random_probability_dist(num_qubits: int) -> dict[int, float]:
    """ Generate a random probability distribution over the measurement outcomes of a quantum circuit with the given number of qubits.
    """
    probability_dist = {}
    for measurement in range(2**num_qubits):
        probability_dist[measurement] = math.random()
    return probability_dist

def generate_random_circuit(num_qubits: int, num_measurements: int) -> QuantumCircuit:
    """ Generate a random quantum circuit with the given number of