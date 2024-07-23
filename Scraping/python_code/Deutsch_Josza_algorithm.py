import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot, draw, show
import os, shutil
from qiskit import BasicAer, IBMQ, QuantumCircuit, ClassicalRegister,\
                    QuantumRegister, execute
from qiskit.compiler import transpile
from qiskit.transpiler import CouplingMap
from qiskit.tools.monitor import job_monitor
from qiskit.tools.visualization import plot_histogram

LaTex_folder_Deutsch_Josza = str(os.getcwd())+'/Latex_quantum_gates/Deutsch_Josza_algorithm/'
if not os.path.exists(LaTex_folder_Deutsch_Josza):
    os.makedirs(LaTex_folder_Deutsch_Josza)
else:
    shutil.rmtree(LaTex_folder_Deutsch_Josza)
    os.makedirs(LaTex_folder_Deutsch_Josza)

n = 4 # number of qubits in state |0>

# Choose a type of oracle at random. 
# With probability one-half it is constant
# and with the same probability it is balanced
oracleType, oracleValue = np.random.randint(2), np.random.randint(2)

if oracleType == 0:
    print("Oracle is constant with value = ", oracleValue)
else:
    print("Oracle is balanced ")
    # this is a hidden parameter for balanced oracles
    a = np.random.randint(1,2**n) 

# Creating registers
# n qubits for querying the oracle and one qubit forstoring the answer
qr = QuantumRegister(n+1, 'q') #all qubits are initialised to |0>

# for recording the measurement on the first register
cr = ClassicalRegister(n, 'c')

circuitName = "DeutschJosza"
djCircuit = QuantumCircuit(qr, cr)

# Create the superposition of all input queries in the first register
# by applying the Hadamard gate to each qubit.
for qubit in qr[0:-2]:
    djCircuit.h(qubit)

# Flip the second register and apply the Hadamard gate
djCircuit.x(qr[n])
djCircuit.h(qr[n])

# Apply the barrier to mark the beginning of the oracle
djCircuit.barrier()

if oracleType == 0:#If the oracleType is "0", the oracle returns oracleValue 
                   #for all inputs
    if oracleValue == 1:
        djCircuit.x(qr[n])
    else:
        djCircuit.id(qr[n])
else: #otherwise, it returns the inner product of the input with 
      #a (non-zero) bitstring
    for i, qubit in enumerate(qr[0:-2]):
        if(a & (1 << i)):
            djCircuit.cx(qubit, qr[n])

# Apply barrier to mark the end of the oracle
djCircuit.barrier()

# Apply Hadamard gates after querying the oracle
for qubit in qr[0:-2]:
    djCircuit.h(qubit)

# Measurement
djCircuit.barrier()
for i in range(n):
    djCircuit.measure(qr[i], cr[i])

# create a LaTex file for the algorithm
LaTex_code = djCircuit.draw(output='latex_source', initial_state=True, justify=None) # draw the circuit
f_name = 'Deutsch_Josza_algorithm.tex'
with open(LaTex_folder_Deutsch_Josza+f_name, 'w') as f:
            f.write(LaTex_code)

## execute on a simulator
backend = BasicAer.get_backend('qasm_simulator')
shots = 1000
job = execute(djCircuit, backend=backend, shots=shots)
results = job.result()
answer = results.get_counts()

plot_histogram(answer)
draw()
show(block=True)

## execute on a real device
provider = IBMQ.load_account()
for backend in IBMQ.providers()[0].backends():
    print(backend.name(),)
backend = provider.backend.ibmq_lima

djCompiled = transpile(djCircuit, backend=backend, optimization_level=1)
djCompiled.draw(output='mpl', scale=0.5)
draw()
show(block=True)

print("This step might take some time!!!")

job = execute(djCompiled, backend=backend, shots=shots)
job_monitor(job)
results = job.result()
answer = results.get_counts()

threshold = int(0.01 *shots) # the threshld of plotting significant measurements
# filter the answer for better view of plots
filteredAnswer = {k: v for k,v in answer.items() if v>= threshold}

# number of counts removed
removedCounts = np.sum([ v for k,v in answer.items() if v < threshold])

# the removed counts are assigned to a new index
filteredAnswer['other_bitstrings'] = removedCounts

plot_histogram(filteredAnswer)
draw()
show(block=True)

# Quantum computers have noise so they would not produce discrete outputs
# like simulators - that only demonstrates the superiority 
# of quantum over classical 

print(filteredAnswer)