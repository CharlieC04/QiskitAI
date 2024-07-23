from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator
from qiskit.transpiler.passes import UnitarySynthesis

circuit = QuantumCircuit(1)
circuit.rx(0.8, 0)
unitary = Operator(circuit).data

unitary_circ = QuantumCircuit(1)
unitary_circ.unitary(unitary, [0])

synth = UnitarySynthesis(basis_gates=["h", "s"], method="sk")
out = synth(unitary_circ)

out.draw('mpl')