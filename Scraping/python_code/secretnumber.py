from qiskit import *
import matplotlib.pyplot as plt
from qiskit.tools.visualization import plot_histogram

secretnumber = '10000100001'

circuit = QuantumCircuit(len(secretnumber) + 1,len(secretnumber))

circuit.h(range(len(secretnumber)))
    
circuit.x(len(secretnumber))
circuit.h(len(secretnumber))

# circuit.draw(output ='mpl')
# plt.show()

circuit.barrier()

# circuit.draw(output ='mpl')
# plt.show()



for i in range(len(secretnumber)):
    if secretnumber[i] == '1':
        circuit.cx(len(secretnumber) - 1 - i, len(secretnumber))
    
# circuit.draw(output ='mpl')
# plt.show()
circuit.barrier()

circuit.h(range(len(secretnumber)))


# circuit.draw(output ='mpl')
# plt.show()

circuit.barrier()

circuit.measure(range(len(secretnumber)),range(len(secretnumber)))


circuit.draw(output ='mpl')
plt.show()

simulator = Aer.get_backend('qasm_simulator')
result = execute(circuit, backend = simulator, shots = 1).result()
counts = result.get_counts()
print(counts)