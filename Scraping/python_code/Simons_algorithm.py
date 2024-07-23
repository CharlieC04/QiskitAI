from qiskit import *
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot, draw, show
import numpy as np
from qiskit.providers.ibmq import least_busy
from qiskit.tools.visualization import plot_histogram
import os, shutil

def dot(s,z):
    sum = 0
    for i in range(len(str(s))):
        sum += int(s[i])*int(z[i])
    return(sum%2)

LaTex_folder_Simon = str(os.getcwd())+'/Latex_quantum_gates/Simon_algorithm/'
if not os.path.exists(LaTex_folder_Simon):
    os.makedirs(LaTex_folder_Simon)
else:
    shutil.rmtree(LaTex_folder_Simon)
    os.makedirs(LaTex_folder_Simon)

s = '10'
s_len = len(str(s))

# create quantum register which is double the size of the secret string
qr = QuantumRegister(s_len, 'q')
qr_ancilla = QuantumRegister(s_len, 'qa')
cr = ClassicalRegister(2*s_len, 'c')

qc = QuantumCircuit(qr, qr_ancilla, cr)

# First Hadamard phase
for qubit in qr:
    qc.h(qubit)

# Apply barrier just to separate
qc.barrier()

# oracle for s
for qubit1 in qr:
    for qubit2 in qr_ancilla:
        qc.cx(qubit1, qubit2)

qc.barrier()

# measure ancilla qubits
for i, qubit in enumerate(qr_ancilla):
    qc.measure(qubit, cr[i+s_len])

qc.barrier()

# another Hadamard phase
for qubit in qr:
    qc.h(qubit)

qc.barrier()

# Measure the input register
for i, qubit in enumerate(qr):
    qc.measure(qubit, cr[i])

qc.draw(output='mpl')
draw()
show(block=True)

# create a LaTex file for the algorithm
LaTex_code = qc.draw(output='latex_source', initial_state=True, justify=None)
f_name = 'Simon_algorithm.tex'
with open(LaTex_folder_Simon+f_name, 'w') as f:
            f.write(LaTex_code)

# simulate
backend = BasicAer.get_backend('qasm_simulator')
shots = 1000
results = execute(qc, backend=backend, shots = shots).result()
answer = results.get_counts()

# Categorise measurements by input register values
answer_plot = {}
for measureresult in answer.keys():
    measureresults_input = measureresult[s_len:]
    if measureresults_input in answer_plot:
        answer_plot[measureresults_input] += answer[measureresult]
    else:
        answer_plot[measureresults_input] = answer[measureresult]

# Plot the categorised results
print(answer_plot)
plt = plot_histogram(answer_plot)
draw()
show(block=True)

# Calculate the dot product of the most significant results
print('s , z , s.z (mod 2)')
for z_rev in answer_plot:
    if answer_plot[z_rev] >= 0.1*shots:
        z = z_rev[::-1]
        print( '{}, {}, {}.{} = {}'.format(s, z, s, z, dot(s,z)))