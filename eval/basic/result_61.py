from qiskit import QuantumRegister, QuantumCircuit, ClassicalRegister
def create_quantum_circuit_with_one_qubit_and_measure():
    """ Build a Quantum Circuit by first creating one Quantum Register and one Classical Register and then perform measurement on it.
    """
    # Create a Quantum Register with one qubit.
    q = QuantumRegister(1)

    # Create a Classical Register with one bit.
    c = ClassicalRegister(1)

    # Create a Quantum Circuit
    circuit = QuantumCircuit(q, c)

    # Add a H gate on qubit 0, putting this qubit in superposition.
    circuit.h(q[0])

    # Add a Measure gate to see the state.
    circuit.measure(q, c)

    return circuit

circuit = create_quantum_circuit_with_one_qubit_and_measure()
circuit.draw(output='mpl')

from qiskit import Aer, execute
backend = Aer.get_backend('qasm_simulator')
job = execute(circuit, backend, shots=1024)
result = job.result()
counts = result.get_counts(circuit)
print(counts)

from qiskit.visualization import plot_histogram
plot_histogram(counts)

# Create a Quantum Register with two qubits.
q = QuantumRegister(2)

# Create a Classical Register