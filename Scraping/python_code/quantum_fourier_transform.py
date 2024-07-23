'''
This program implements the quantum Fourier transform (QFT)
'''

from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, IBMQ
from qiskit.visualization import circuit_drawer as drawer
from qiskit.tools.visualization import plot_histogram
from qiskit import execute
from qiskit import Aer

import numpy as np
import time, os, shutil
from matplotlib.pyplot import plot, draw, show

def QFT(q, c, n):
    qc = QuantumCircuit(q,c)
    # First get the most significant bit
    for k in range(n):
        j = n - k

        # now add the Hadamard transform to qubit j-1
        qc.h(q[j-1])
        
        # now each qubit from the lowest significance 
        # takes one conditional phase shift
        for i in reversed(range(j-1)):
            qc.cp(2*np.pi/2**(j-i), q[i], q[j-1])
    
    # Finally swap the qubits
    for i in range(n//2):
        qc.swap(q[i], q[n-i-1])
    return qc

# QFT is represented in a matrix form with 2^n rows and columns
# where n represents the number of qubits

def QFTmatrix(n):
    qft = np.zeros([2**n,2**n], dtype=complex)
    for i in range(2**n):
        for k in range(2**n):
            qft[i,k] = np.exp(i*k*2*2j*np.pi/(2**n))
    return(1/np.sqrt(2**n)*qft)

def QFTcircuit(n):
    q = QuantumRegister(n, "q")
    c = ClassicalRegister(n, "c")
    qc = QFT(q, c, n)
    backend = Aer.get_backend('unitary_simulator')
    job = execute(qc, backend)
    actual = job.result().get_unitary()
    np.around(actual, 2)
    expected = QFTmatrix(n)
    delta = actual - expected
    print("Deviation: ", round(np.linalg.norm(delta), 10))

    return qc

LaTex_folder_QFT = str(os.getcwd())+'/Latex_quantum_gates/Quantum_Fourier_transform/'
if not os.path.exists(LaTex_folder_QFT):
    os.makedirs(LaTex_folder_QFT)
else:
    shutil.rmtree(LaTex_folder_QFT)
    os.makedirs(LaTex_folder_QFT)

n=4
qc = QFTcircuit(n)
# create a LaTex file for the algorithm
LaTex_code = qc.draw(output='latex_source', initial_state=True, justify=None) # draw the circuit
f_name = 'Quantum_Four_transform_'+str(n)+'qubits.tex'
with open(LaTex_folder_QFT+f_name, 'w') as f:
            f.write(LaTex_code)

n = 4
q = QuantumRegister(n, "x")
c = ClassicalRegister(n, "c")
qftCircuit = QFT(q, c, n)
initCircuit = QuantumCircuit(q, c)
for qubit in q:
    initCircuit.h(qubit)

initCircuit.barrier(q)
qc = QuantumCircuit.compose(initCircuit, qftCircuit)
qc.barrier(q)
qc.measure(q, c)

# on simulator
backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend)
k = job.result().get_counts()

print(k)

# on a real quantum computer
provider = IBMQ.load_account()
backend = provider.backend.ibmq_lima

print("Status of backened: ", backend.status())
job = execute(qc, backend=backend, shots = 1024)
lapse = 0

print("This step might take some time.")

time.sleep(3)
interval = 60
while((job.status().name != 'DONE') 
    and (job.status().name != 'Cancelled')
    and (job.status().name != 'ERROR')):

    print('Status @ {} seconds'.format(interval * lapse))
    print(job.status())
    print(job.queue_position())
    time.sleep(interval)
    lapse +=1
print(job.status())
plt = plot_histogram(job.result().get_counts())