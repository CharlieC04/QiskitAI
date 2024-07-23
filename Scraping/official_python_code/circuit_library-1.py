from qiskit.circuit.library import MCXGate
gate = MCXGate(4)

from qiskit import QuantumCircuit
circuit = QuantumCircuit(5)
circuit.append(gate, [0, 1, 4, 2, 3])
circuit.draw('mpl')