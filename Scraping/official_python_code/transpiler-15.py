from qiskit import QuantumCircuit

ghz = QuantumCircuit(5)
ghz.h(0)
ghz.cx(0,range(1,5))
ghz.draw(output='mpl')