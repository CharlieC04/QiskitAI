# HONR 293W Quantum Computing for Fun Clayton Grubick
# complete program written in Qiskit for searching a
# two-qubit quantum database using Grover’s search
# algorithm.
# 

from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_histogram
from numpy import random
from matplotlib import pyplot as plt
def DB_function(QC, color_code):
#if color_code == 0: do nothing
    if color_code == 1: 
        QC.ccx(0,1,3)
    elif color_code == 2: 
        QC.ccx(0,1,2)
    elif color_code == 3:
        QC.ccx(0,1,2)
        QC.ccx(0,1,3)
color_codes =  [0,1,2,3]
random.shuffle(color_codes)
database = {}
for i in range(4):
    database[i]= color_codes[i]
desired_color_code = 2
DB = QuantumCircuit(5)
#for when index = 0 = 00
DB.x(0)
DB.x(1)
DB_function(DB, database[0])
DB.x(0)
DB.x(1)
#for when index = 1 =  01
DB.x(0)
DB_function(DB, database[1])
DB.x(0)
#for when index = 2 = 10
DB.x(1)
DB_function(DB, database[2])
DB.x(1)
#for when index = 3 = 11
DB_function(DB, database[3])
MG = QuantumCircuit(5)
if desired_color_code == 0:
    MG.x(2)
    MG.x(3)
    MG.ccx(2,3,4)
    MG.x(2)
    MG.x(3)
elif desired_color_code == 1:
    MG.x(2)
    MG.ccx(2,3,4)
    MG.x(2)
elif desired_color_code == 2:
    MG.x(3)
    MG.ccx(2,3,4)
    MG.x(3)
elif desired_color_code == 3:
    MG.ccx(2,3,4)
oracle = QuantumCircuit(5)
oracle.compose(DB, inplace=True)
oracle.compose(MG, inplace=True)
oracle.compose(DB, inplace=True)
phase = QuantumCircuit(5)
phase.x(0)
phase.x(1)
phase.h(1)
phase.cx(0,1)
phase.h(1)
phase.x(0)
phase.x(1)
Grover = QuantumCircuit(5)
Grover.compose(oracle, inplace=True)
Grover.h(0)
Grover.h(1)
Grover.compose(phase, inplace=True)
Grover.h(0)
Grover.h(1)
circuit = QuantumCircuit(5,2)
circuit.x(4)
circuit.h(0)
circuit.h(1)
circuit.h(4)
circuit.compose(Grover, inplace=True)
circuit.measure(0,1)
circuit.measure(1,0)
sim = Aer.get_backend('qasm_simulator')
results = execute(circuit,sim,shots = 1000)
counts = results.result().get_counts()
print("Done")
plot_histogram(counts)
plt.show()