from qiskit.quantum_info import Operator
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.synthesis import LieTrotter
from qiskit import QuantumCircuit
from qiskit.quantum_info import Pauli, SparsePauliOp
def create_product_formula_circuit(pauli_strings: list, times: list, order: int, reps: int) -> QuantumCircuit:
    """ Create a quantum circuit using LieTrotter for a list of Pauli strings and times. Each Pauli string is associated with a corresponding time in the 'times' list. The function should return the resulting QuantumCircuit.
    """
    # Create a QuantumCircuit with the specified number of qubits
    qc = QuantumCircuit(len(pauli_strings[0]))

    # Create a LieTrotter circuit for each Pauli string and time
    for i in range(len(pauli_strings)):
        pauli_string = pauli_strings[i]
        time = times[i]
        ltc = LieTrotter(PauliEvolutionGate(Operator(pauli_string)), time, order=order, reps=reps)
        qc.compose(ltc, inplace=True)

    return qc

pauli_strings = ["X", "Y", "Z"]
times = [1, 2, 3]
order = 2
reps = 1
qc = create_product_formula_circuit(pauli_strings, times, order, reps)
qc.draw()

pauli_strings = ["X", "Y", "Z"]
times = [1, 2, 3]
order = 2
reps = 2
qc = create_product_formula_circuit(pauli_strings, times, order,