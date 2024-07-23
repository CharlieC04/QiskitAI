'''
This program performs the Berstein-Vazirani algorithm to guess a secret code
'''
from qiskit import *
from qiskit.visualization import plot_histogram
from matplotlib.pyplot import plot, draw, show
import numpy as np
import os, shutil

LaTex_folder_Berstein_Vazirani = str(os.getcwd())+'/Latex_quantum_gates/Berstein_Vazarani/'
if not os.path.exists(LaTex_folder_Berstein_Vazirani):
    os.makedirs(LaTex_folder_Berstein_Vazirani)
else:
    shutil.rmtree(LaTex_folder_Berstein_Vazirani)
    os.makedirs(LaTex_folder_Berstein_Vazirani)

## guess a secret binary number

s = '110101' #secret number/code
n = len(s)
qc = QuantumCircuit(n+1,n)
qc.x(n)
qc.barrier()
qc.h(range(n+1))
qc.barrier()

# to separate steps
for i, tf in enumerate(reversed(s)):
    if(tf == '1'):
        qc.cx(i,n)

qc.barrier()
qc.h(range(n+1))
qc.barrier()
qc.measure(range(n), range(n))

# create a LaTex file for the algorithm
LaTex_code = qc.draw(output='latex_source', initial_state=True, justify=None) # draw the circuit
f_name = 'Berstein_Vazirani.tex'
with open(LaTex_folder_Berstein_Vazirani+f_name, 'w') as f:
            f.write(LaTex_code)

# simulate the algorithm
simulator = Aer.get_backend('qasm_simulator')
job = execute(qc, simulator, shots=1)
results = job.result()
count = results.get_counts()
plot_histogram(results.get_counts(qc))
print(count)
draw()
show(block=True)

## guess a secret string
string = 'Thank you for the nice book'
bit_string = []

# convert string to bit-string
for c in string:
    bits_letter = format(ord(c), 'b')
    for bit in bits_letter:
        bit_string.append(bit)

n = len(bit_string)
qc = QuantumCircuit(n+1,n)
qc.x(n)
qc.barrier()
qc.h(range(n+1))
qc.barrier()

# to separate steps
for i, tf in enumerate(reversed(bit_string)):
    if(tf == '1'):
        qc.cx(i,n)

qc.barrier()
qc.h(range(n+1))
qc.barrier()
qc.measure(range(n), range(n))

simulator = Aer.get_backend('qasm_simulator')
job = execute(qc, simulator, shots=1)
results = job.result()
count = results.get_counts()
plot_histogram(results.get_counts(qc))
print(len(bit_string),'\n', count)
draw()
show(block=True)