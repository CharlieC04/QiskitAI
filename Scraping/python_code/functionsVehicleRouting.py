import numpy as np
from qiskit import Aer
from qiskit import QuantumCircuit
from VehicleRouting.standard.CostCalculator import CostCalculator


def compute_expectation(counts, graph):
    """
    Computes expectation value based on measurement results

    Args:
        counts: dict
                key as bitstring, val as count

        graph: networkx graph

    Returns:
        avg: float
             expectation value
    """

    sum_cost = 0
    sum_count = 0
    for bitstring, count in counts.items():
        cost_calculator = CostCalculator(bitstring, graph, 1, 100)
        cost = cost_calculator.vehicle_routing_cost()
        sum_cost += cost * count
        sum_count += count

    expectation_value = sum_cost / sum_count
    return expectation_value


# We will also bring the different circuit components that
# build the qaoa circuit under a single function
def create_qaoa_circuit(graph, theta):
    """
    Creates qaoa circuit

    Args:
        graph: networkx graph
        theta: qaoa parameters
    """
    number_of_nodes = len(graph.nodes())
    number_of_qubits = number_of_nodes * (number_of_nodes-1) # n*(n-1)
    precision = len(theta) // 2  # number of alternating unitaries p
    quantum_circuit = QuantumCircuit(number_of_qubits)

    beta = theta[:precision]
    gamma = theta[precision:]

    # initial_state
    for index_qubit in range(0, number_of_qubits):
        quantum_circuit.h(index_qubit)

    quantum_circuit.barrier()

    for index_repetition in range(0, precision):

        # problem unitary
        for i in range(0, number_of_qubits):
            for j in range(0, i):
                J = 1
                quantum_circuit.rzz(2* gamma[index_repetition], i, j)

        quantum_circuit.barrier()

        for i in range(0, number_of_qubits):
            quantum_circuit.rz(2 * gamma[index_repetition], i)

        quantum_circuit.barrier()

        # mixer unitary
        for index_qubit in range(0, number_of_qubits):
            quantum_circuit.rxx(2 * beta[index_repetition], index_qubit,np.mod(index_qubit+1,number_of_qubits))
            quantum_circuit.ryy(2 * beta[index_repetition], index_qubit,np.mod(index_qubit+1,number_of_qubits))
        quantum_circuit.barrier()

    # measure
    quantum_circuit.measure_all()

    return quantum_circuit



# Finally we write a function that executes the circuit on the chosen backend
def get_execute_circuit(graph, shots=512):
    """
    Runs parametrized circuit

    Args:
        graph: networkx graph
    """
    backend = Aer.get_backend('qasm_simulator')
    backend.shots = shots

    def execute_circuit(theta):
        quantum_circuit = create_qaoa_circuit(graph, theta)
        counts = backend.run(quantum_circuit, seed_simulator=10,
                             nshots=2 ^ 12).result().get_counts()

        return compute_expectation(counts, graph)

    return execute_circuit
