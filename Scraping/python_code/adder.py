'''
This program sets up the Half Adder and the Full Adder and creates a .tex file
with the gate geometry. It also evaluates the result with a qasm quantum 
simulator
'''

from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, \
                    execute, result, Aer
import os
import shutil
import numpy as np
import lib.adder as adder
import lib.quantum_logic as logic

LaTex_folder_Adder_gates = str(os.getcwd())+'/Latex_quantum_gates/Adder-gates/'
if not os.path.exists(LaTex_folder_Adder_gates):
    os.makedirs(LaTex_folder_Adder_gates)
else:
    shutil.rmtree(LaTex_folder_Adder_gates)
    os.makedirs(LaTex_folder_Adder_gates)

qubit_space = ['0','1']

## Half Adder (my version)
print("Test Half Adder (my version",'\n')

for add0 in qubit_space: # loop over all possible additions
    for add1 in qubit_space:            
        q  = QuantumRegister(3, name = 'q')
        c  = ClassicalRegister(2, name = 'c')
        qc = QuantumCircuit(q,c)
        for qubit in q:
            qc.reset(qubit)

        # initialisation
        if(add0== '1'):
            qc.x(q[0])
        if(add1 == '1'):
            qc.x(q[1])

        adder.Half_Adder(qc, q[0],q[1],q[2])
        qc.measure(q[0], c[0])
        qc.measure(q[2], c[1])

        backend = Aer.get_backend('qasm_simulator')
        job = execute(qc, backend, shots=1000)
        results = job.result()
        count = results.get_counts()
        print('|0', add0, '>', '+', '|0', add1, '>', '\t', count)

## Plot a sketch of the gate
q  = QuantumRegister(3, name = 'q')
c  = ClassicalRegister(2, name = 'c')
qc = QuantumCircuit(q,c)

qc.reset(q[2])
adder.Half_Adder(qc, q[0],q[1],q[2])
qc.measure(q[1], c[0])
qc.measure(q[2], c[1])

LaTex_code = qc.draw(output='latex_source',
                     justify=None) # draw the circuit
f_name = 'Half_Adder_gate_Benjamin.tex'
with open(LaTex_folder_Adder_gates+f_name, 'w') as f:
            f.write(LaTex_code)

## Half Adder for two qubits (Beyond Classical book version)
print("Test Half Adder Beyond Classical")
for add0 in qubit_space: # loop over all possible additions
    for add1 in qubit_space:  
        q  = QuantumRegister(5, name = 'q')
        c  = ClassicalRegister(2, name = 'c')
        qc = QuantumCircuit(q,c)
        
        # initialisation
        if(add0 == '1'):
            qc.x(q[0])
        if(add1 == '1'):
            qc.x(q[1])

        logic.XOR(qc, q[0],q[1],q[2])
        qc.barrier(q)

        logic.AND(qc, q[0], q[1], q[3])
        qc.barrier(q)

        qc.measure(q[2], c[0])
        qc.measure(q[3], c[1])

        backend = Aer.get_backend('qasm_simulator')
        job = execute(qc, backend, shots=1000)
        results = job.result()
        count = results.get_counts()
        print('|0', add0, '>', '+', '|0', add1, '>', '\t', count)
        if(add0=='0' and add1=='1'):
            LaTex_code = qc.draw(output='latex_source', justify=None) # draw the circuit
            f_name = 'Half_Adder_gate_Beyond_Classical.tex'
            with open(LaTex_folder_Adder_gates+f_name, 'w') as f:
                        f.write(LaTex_code)

## Full Adder for addition of two-qubits |q1>, |q2>, and a carry bit |qd>
#  from another calculation using a anxiliary bit |q0> with a carry qubit |cq>
#  which is initialised to |0>  
# iteration over all possible values for |q1>, |q2>, and |qd>
print('\n',"Full Adder Test (my version)")
for qubit_2 in qubit_space:
    for qubit_1 in qubit_space:
        for qubit_d in qubit_space:
            string_q1 = str(qubit_1)
            string_q2 = str(qubit_2)
            string_qd = str(qubit_d)

            q1  = QuantumRegister(1, name ='q1')
            q2  = QuantumRegister(1, name = 'q2')
            qd  = QuantumRegister(1, name = 'qd')
            q0  = QuantumRegister(1, name = 'q0')
            c   = ClassicalRegister(2, name = 'c')
            qc  = QuantumCircuit(q1,q2,qd,q0,c)

            for qubit in q1:
                qc.reset(qubit)
            for qubit in q2:
                qc.reset(qubit)
            for qubit in qd:
                qc.reset(qubit)
            for qubit in q0:
                qc.reset(qubit)
            
            # initialise qubits which should be added
            for i, qubit in enumerate(q1):
                if(string_q1[i] == '1'):
                    qc.x(qubit)
                    print(1,end="")
                else:
                    print(0,end="")
            print('\t',end="")
            for i, qubit in enumerate(q2):
                if(string_q2[i] == '1'):
                    qc.x(qubit)
                    print(1,end="")
                else:
                    print(0,end="")
            print('\t',end="")
            for i, qubit in enumerate(qd):
                if(string_qd[i] == '1'):
                    qc.x(qubit)
                    print(1,end="")
                else:
                    print(0,end="")
            print('\t',end="")

            adder.Full_Adder(qc, q1, q2, qd, q0, c[0])
            qc.measure(q0, c[1])
            
            # check the results
            backend = Aer.get_backend('qasm_simulator')
            job = execute(qc, backend, shots=1000)
            results = job.result()
            count = results.get_counts()
            print('|', qubit_1, '>', '+', '|', qubit_2, '>', '+', '|', qubit_d, '> = ' , '\t', count)

            if(qubit_1 == '0' and qubit_2 == '0' and qubit_d == '0'):
                LaTex_code = qc.draw(output='latex_source') # draw the circuit
                f_name = 'Full_Adder_gate_Benjamin.tex'
                with open(LaTex_folder_Adder_gates+f_name, 'w') as f:
                            f.write(LaTex_code)

## Test for adding two two-qubit numbers |q1> and |q2>
for qubit1_0 in qubit_space:
    for qubit1_1 in qubit_space:
        for qubit2_0 in qubit_space:
            for qubit2_1 in qubit_space:
                string_q1 = str(qubit1_1)+str(qubit1_0)
                string_q2 = str(qubit2_1)+str(qubit2_0)
                
                q1  = QuantumRegister(2, name ='q1')
                q2  = QuantumRegister(2, name = 'q2')

                # qubit to store carry over for significiant bit
                q0  = QuantumRegister(1, name = 'q0') 
                
                c   = ClassicalRegister(3, name = 'c')
                qc  = QuantumCircuit(q1,q2,q0,c)
                
                for qubit in q1:
                    qc.reset(qubit)
                qc.reset(q2)
                qc.reset(q0)    
                
                # initialise qubits which should be added
                for i, qubit in enumerate(q1):
                    if(string_q1[i] == '1'):
                        qc.x(qubit)
                        print(1,end="")
                    else:
                        print(0,end="")
                print('\t',end="")
                for i, qubit in enumerate(q2):
                    if(string_q2[i] == '1'):
                        qc.x(qubit)
                        print(1,end="")
                    else:
                        print(0,end="")
                print('\t',end="")

                adder.Half_Adder(qc,q1[-1],q2[-1],q0)
                qc.measure(q2[-1],c[0])
                adder.Full_Adder(qc, q1[-2],q2[-2], q0, q2[-1], c[1])
                qc.measure(q2[-1], c[2])
                
                # check the results
                backend = Aer.get_backend('qasm_simulator')
                job = execute(qc, backend, shots=1000)
                results = job.result()
                count = results.get_counts()
                print('|', qubit1_1, qubit1_0, '>', '+', '|', qubit2_1, 
                        qubit2_0, '> = ' , '\t', count)

                if(qubit1_1 == '0' and qubit1_0 == '1' 
                 and qubit2_1 == '0' and qubit2_0 == '0'):
                    LaTex_code = qc.draw(output='latex_source') # draw the circuit
                    # export QASM code
                    qc.qasm(filename="one_plus_one.qasm")
                    f_name = 'Adder_gate_for_two_two-qubit_numbers.tex'
                    with open(LaTex_folder_Adder_gates+f_name, 'w') as f:
                                f.write(LaTex_code)

## Adder for two arbitrary binary numbers
# randomly draw number of bits from the numbers to add
bit_number_q1 = int(np.ceil(10*np.random.rand()))+2
bit_number_q2 = int(np.ceil(10*np.random.rand()))+2

# prepare two random binary numbers
string_q1 = []
string_q2 = []

for i in range(bit_number_q1):
    #string_q1.append(1)
    string_q1.append(int(np.round(np.random.rand())))
for i in range(bit_number_q2):
    string_q2.append(int(np.round(np.random.rand())))

while(len(string_q1)<len(string_q2)):
    string_q1 = np.insert(string_q1, 0, 0, axis=0)

  
while(len(string_q1)>len(string_q2)):
    string_q2 = np.insert(string_q2, 0, 1, axis=0)

string_q1 = np.array(string_q1)
string_q2 = np.array(string_q2)

q1  = QuantumRegister(len(string_q1), name = 'q1')
q2  = QuantumRegister(len(string_q2), name = 'q2')

# qubit to store carry over for initial half adder
q0  = QuantumRegister(1, name = 'q0') 

c   = ClassicalRegister(len(string_q1)+1, name = 'c')
qc  = QuantumCircuit(q1,q2,q0,c)

for qubit in q1:
    qc.reset(qubit)

for qubit in q2:
    qc.reset(qubit)

qc.reset(q0)


# initialise qubits which should be added
for i, qubit in enumerate(q1):
    if(string_q1[i] == 1):
        qc.x(qubit)
        print(1,end="")
    else:
        print(0,end="")
print('\n',end="")
for i, qubit in enumerate(q2):
    if(string_q2[i] == 1):
        qc.x(qubit)
        print(1,end="")
    else:
        print(0,end="")
print('\n')

# initial addition of least significant bits and determining carry bit
adder.Half_Adder(qc, q1[-1], q2[-1], q0)
qc.measure(q2[-1], c[0])

# adding of next significant bits
adder.Full_Adder(qc, q1[-2], q2[-2], q0, q2[-1], c[1])

# adding of other digits by full adder cascade
for i in range(2, len(string_q1)):
    adder.Full_Adder(qc,
                    q1[-i-1], # bit to add
                    q2[-i-1], # bit to add 
                              #(and to measure as next significant bit)
                    q2[-i+1],   # carry from last calculation
                    q2[-i], # carry for next calculation
                    c[i])
qc.measure(q2[-len(string_q1)+1], c[len(string_q1)])

# check the results
backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend, shots=10)
results = job.result()
count = results.get_counts()
print(count)

LaTex_code = qc.draw(output='latex_source') # draw the circuit
f_name = 'Adder_gate_for_'+str(string_q1)+'_and_'+str(string_q2)+'.tex'
print(f_name)
with open(LaTex_folder_Adder_gates+f_name, 'w') as f:
            f.write(LaTex_code)