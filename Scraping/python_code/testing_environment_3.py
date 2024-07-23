import numpy as np
from matplotlib import pyplot as plt
from qiskit import QuantumCircuit, Aer, transpile, assemble
from qiskit.circuit import Gate
from qiskit.circuit import Parameter
from qiskit.extensions import UnitaryGate, HamiltonianGate
from qiskit.providers.aer import StatevectorSimulator
from qiskit.visualization import plot_histogram
from qiskit_nature.operators.second_quantization import SpinOp

from VehicleRouting.standard.concretization.CircuitPlotter import MPLCircuitPlotter

beta = Parameter('beta')
spinop = SpinOp([("++--", 1),("--++", 1)])
print(spinop.to_matrix())

gate = HamiltonianGate(spinop.to_matrix(), np.pi/2, label="Gate")
qc = QuantumCircuit(4)
qc.h(0)
qc.h(1)
qc.h(2)
qc.h(3)


qc.append(gate, [0,1,2,3])



backend = StatevectorSimulator(precision='double')
transpiled = transpile(qc, backend=backend)
transpiled.draw('mpl')
result = backend.run(transpiled).result()
counts = result.get_counts()

print(result)
print(counts)
plot_histogram(counts)

circuit_plotter = MPLCircuitPlotter()
circuit_plotter.plot(qc)
plt.show()
