from qiskit import *
from qiskit.tools.visualization import plot_bloch_multivector
import matplotlib.pyplot as plt


qr = QuantumRegister(1)
cr = ClassicalRegister(1)

circuit = QuantumCircuit(qr, cr)

circuit.x(0)

#simulator = Aer.get_backend('statevector_simulator')
simulator = Aer.get_backend('unitary_simulator')

result = execute(circuit, backend=simulator).result()

#statevector = result.get_statevector()
unitary = result.get_unitary()

#plot_bloch_multivector(statevector)
#plt.show()

circuit.measure(qr, cr)

#backend = Aer.get_backend('qasm_simulator')

#result = execute(circuit, backend=backend, shots=1024).result()

#counts = result.get_counts()

from qiskit.tools.visualization import plot_histogram

plot_histogram(result.get_counts(circuit))
plt.show()

#print(statevector)
#print(circuit)
print(unitary)