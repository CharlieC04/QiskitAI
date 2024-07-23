'''
This code creates the gates for all four Bell states 
and prints the LaTex code for the circuit 
'''
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
import os
import shutil

use_classical_register = True
LaTex_folder_Bell_states = str(os.getcwd())+'/Latex_quantum_gates/Bell_measurement/'
if not os.path.exists(LaTex_folder_Bell_states):
    os.makedirs(LaTex_folder_Bell_states)
else:
    shutil.rmtree(LaTex_folder_Bell_states)
    os.makedirs(LaTex_folder_Bell_states)

qr = QuantumRegister(2) # initialise a two-bit quantum register
cr = ClassicalRegister(2) # initialise a two-bit classical register
if(not use_classical_register):
    circuit = QuantumCircuit(qr) # put only quantum registers into circuit
else:
    circuit = QuantumCircuit(qr, cr) # put classical and quantum registers into circuit
circuit.cx(qr[0],qr[1]) # at a CNOT gate to the second qubit depending on the state of the first one        
circuit.h(qr[0]) # add a Hadamard gate to first qubit
if(use_classical_register):
    circuit.measure(qr,cr) # measure the quantum bits

LaTex_code = circuit.draw(output='latex_source', initial_state=True, justify=None) # draw the circuit
f_name = 'Bell_state_measurement.tex'

with open(LaTex_folder_Bell_states+f_name, 'w') as f:
    f.write(LaTex_code)
