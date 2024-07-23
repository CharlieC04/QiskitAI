import qiskit as qis
from qiskit.tools.visualization import plot_bloch_multivector
import matplotlib.pyplot as plt
from qiskit.tools.visualization import plot_histogram
import math as math

# Define Registers
qr = qis.QuantumRegister(1)
cr = qis.ClassicalRegister(1)

# Make Circuit
circuit = qis.QuantumCircuit(qr, cr)

# Make Gates and Circuit Additions
#circuit.cz(qr[0], qr[1])
circuit.x(qr[0])
#circuit.x(qr[1])
#circuit.cswap(qr[0], qr[1], qr[2])
#circuit.ccx(qr[0], qr[1], qr[2])
#circuit.h(qr[0])
#circuit.cx(qr[0], qr[1])
#circuit.rx(math.pi/2, qr[0])
#circuit.swap(qr[0], qr[1])

# Choose Unitary Simulator
simulator = qis.Aer.get_backend('unitary_simulator')

# Get Unitary Results (Multiplication of all Gates/Additions)
result = qis.execute(circuit, backend=simulator).result()
unitary = result.get_unitary()

# Plot Unitary Results
print(unitary)

# Choose Statevector Simulator
simulator = qis.Aer.get_backend('statevector_simulator')

# Get Statevector Results
result = qis.execute(circuit, backend=simulator).result()
statevector = result.get_statevector()

# Plot Statevector Results
plot_bloch_multivector(statevector)

# Measure Qubits to Classical
circuit.measure(qr, cr)

# Print Circuit (Along w/ Measurements)
print(circuit)
#circuit.draw(output='mpl')

# Choose Qasm Simulator
simulator = qis.Aer.get_backend('qasm_simulator')

# Get Qasm Results
result = qis.execute(circuit, backend=simulator).result()

# Plot Qasm Measurements
plot_histogram(result.get_counts(circuit))
plt.show()
