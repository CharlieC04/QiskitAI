from qiskit import QuantumCircuit, transpile

ghz = QuantumCircuit(15)
ghz.h(0)
ghz.cx(0, range(1, 15))
ghz.draw(output='mpl')