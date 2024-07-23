from qiskit import*
import matplotlib.pyplot as plt
from qiskit.extensions import Initialize
from qiskit.tools.visualization import plot_bloch_multivector
from qiskit_textbook.tools import random_state


circuit = QuantumCircuit(3,2)
psi = random_state(1)
plot_bloch_multivector(psi)

init_gate = Initialize(psi)
print(f'\psi = {psi}')
init_gate.label = 'Estado inicial'

circuit.append(init_gate, [0])
circuit.barrier()

circuit.h(1)
circuit.cx(1,2)
circuit.barrier()

circuit.cx(0,1)
circuit.h(0)

circuit.barrier()
circuit.measure([0,1], [0,1])   # fazer as medidas de q0 e q1 e armazenar nos bits 0 e 1

circuit.barrier()

circuit.cx(1,2)
circuit.cz(0,2)

circuit.draw(output ='mpl')

simulator = Aer.get_backend('qasm_simulator')
circuit.save_statevector()
result = simulator.run(circuit).result().get_statevector()
plot_bloch_multivector(result)
plt.show()
