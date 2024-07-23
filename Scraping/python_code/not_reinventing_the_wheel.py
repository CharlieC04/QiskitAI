from qiskit.synthesis import QDrift
from qiskit.circuit.library import PauliEvolutionGate
from qiskit import QuantumCircuit
from qiskit.quantum_info import Pauli


# Define the Hamiltonian
XX = Pauli('XX')
YY = Pauli('YY')
ZZ = Pauli('ZZ')
a = 1
b = -1
c = 1
# A simple Hamiltonian: a XX + b YY + c ZZ. Use the appropriate Pauli compose method to do this.
hamiltonian = a * XX.compose(b*ZZ)
reps = 10
time = 1

evo_gate = PauliEvolutionGate(hamiltonian, time, synthesis=QDrift(reps=reps))

qc = QuantumCircuit(2)
qc.append(evo_gate, [0, 1])

qc.draw('mpl')


