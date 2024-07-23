# useful additional packages
import matplotlib.pyplot as plt
#%matplotlib inline
import numpy as np
from pprint import pprint

# importing QISKit
from qiskit import QuantumProgram, QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import available_backends, execute, register, least_busy

# import basic plot tools
from qiskit.tools.visualization import plot_histogram, circuit_drawer

qx_config = {
  "APItoken": 'dcdb2d9414a625c1f57373c544add3711c78c3d7faf39397fe2c41887110e8b59caf81bcb2bc32714d936da41a261fea510f96df379afcbdfa9df6cc6bfe3829',
    "url": 'https://quantumexperience.ng.bluemix.net/api'
}

backend = 'local_qasm_simulator' # run on local simulator by default
'''register(qx_config['APItoken'], qx_config['url'])
backend = least_busy(available_backends({'simulator': False, 'local': False}))
print("the best backend is " + backend)
'''
# Creating registers
q2 = QuantumRegister(2)
c2 = ClassicalRegister(2)

# quantum circuit to make an entangled bell state
bell = QuantumCircuit(q2, c2)
bell.h(q2[0])
bell.cx(q2[0], q2[1])

# quantum circuit to measure q0 in the standard basis
measureIZ = QuantumCircuit(q2, c2)
measureIZ.measure(q2[0], c2[0])
bellIZ = bell+measureIZ

# quantum circuit to measure q0 in the superposition basis
measureIX = QuantumCircuit(q2, c2)
measureIX.h(q2[0])
measureIX.measure(q2[0], c2[0])
bellIX = bell+measureIX

# quantum circuit to measure q1 in the standard basis
measureZI = QuantumCircuit(q2, c2)
measureZI.measure(q2[1], c2[1])
bellZI = bell+measureZI

# quantum circuit to measure q1 in the superposition basis
measureXI = QuantumCircuit(q2, c2)
measureXI.h(q2[1])
measureXI.measure(q2[1], c2[1])
bellXI = bell+measureXI

# quantum circuit to measure q in the standard basis
measureZZ = QuantumCircuit(q2, c2)
measureZZ.measure(q2[0], c2[0])
measureZZ.measure(q2[1], c2[1])
bellZZ = bell+measureZZ

# quantum circuit to measure q in the superposition basis
measureXX = QuantumCircuit(q2, c2)
measureXX.h(q2[0])
measureXX.h(q2[1])
measureXX.measure(q2[0], c2[0])
measureXX.measure(q2[1], c2[1])
bellXX = bell+measureXX

# quantum circuit to make a mixed state
mixed1 = QuantumCircuit(q2, c2)
mixed2 = QuantumCircuit(q2, c2)
mixed2.x(q2)
mixed1.h(q2[0])
mixed1.h(q2[1])
mixed1.measure(q2[0], c2[0])
mixed1.measure(q2[1], c2[1])
mixed2.h(q2[0])
mixed2.h(q2[1])
mixed2.measure(q2[0], c2[0])
mixed2.measure(q2[1], c2[1])

'''circuits = [bellIZ,bellIX,bellZI,bellXI,bellZZ,bellXX]
job = execute(circuits, backend)
result = job.result()
print(result.get_counts(bellXX))
plot_histogram(result.get_counts(bellXX))'''

mixed_state = [mixed1,mixed2]
job = execute(mixed_state, backend)
result = job.result()

counts1 = result.get_counts(mixed_state[0])
counts2 = result.get_counts(mixed_state[1])

from collections import Counter
ground = Counter(counts1)
excited = Counter(counts2)
plot_histogram(ground+excited)