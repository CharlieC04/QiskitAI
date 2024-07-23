'''
This is a implementation of the quantum teleportation algorithm
'''

from qiskit import *
from qiskit.visualization import plot_histogram
import os, shutil, numpy
from matplotlib.pyplot import plot, draw, show

LaTex_folder_Quantum_Teleportation = str(os.getcwd())+'/Latex_quantum_gates/Quantum_Teleportation/'
if not os.path.exists(LaTex_folder_Quantum_Teleportation):
    os.makedirs(LaTex_folder_Quantum_Teleportation)
else:
    shutil.rmtree(LaTex_folder_Quantum_Teleportation)
    os.makedirs(LaTex_folder_Quantum_Teleportation)

qc = QuantumCircuit(3,3)
## prepare the state to be teleported
phi = 0*numpy.pi
theta= 0.5*numpy.pi
lam = 0*numpy.pi
qc.u(phi=phi, theta=theta,lam=lam,qubit=0)

## teleport the state
qc.barrier()
qc.h(1)
qc.cx(1,2)
qc.cz(0,1)
qc.h(0)
qc.h(1)
qc.barrier()
qc.measure([0,1],[0,1])
qc.barrier()
qc.x(2).c_if(0,1)
qc.z(2).c_if(1,1)
qc.h(2)
qc.measure(2,2)

LaTex_code = qc.draw(output='latex_source', initial_state=True, justify=None) # draw the circuit
f_name = 'quantum_teleportation.tex'
with open(LaTex_folder_Quantum_Teleportation+f_name, 'w') as f:
            f.write(LaTex_code)

# simulation
simulator = Aer.get_backend('qasm_simulator')
result = execute(qc, backend=simulator, shots=100000).result()
counts = {'0':0,
           '1': 0}
print(result.get_counts().keys())
for key, value in result.get_counts().items():
    if(key[0] == '0'):
          counts['0'] += value
    else:
          counts['1'] += value
print(counts)
plt = plot_histogram(counts)
draw()
show(block=True)