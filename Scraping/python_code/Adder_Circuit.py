from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute
from qiskit import BasicAer                                                  
'''
APItoken="APItoken"                
config = { "url": 'https://quantumexperience.ng.bluemix.net/api'}
'''
n1 = input("Enter a binary number with less than 8 digits:")
n2 = input("Enter another binary number with less than 8 digits:")
l1 = len(n1)
l2 = len(n2)
n = 0
if l1>l2:                                           
    n = l1
else:
    n = l2
a = QuantumRegister(n)                              #First number
b = QuantumRegister(n+1)                            #Second number
c = QuantumRegister(n)                              #Carry bits
cl = ClassicalRegister(n+1)                         #Clasical register to store the value of qubits
qc = QuantumCircuit(a,b,c,cl)                       #Creating a quantum circuit using quantum registers and classical registers
for i in range(l1):             
    if n1[i] == "1":            
        qc.x(a[l1-(i+1)])                           #Changing all qubits corresponding to 1 in the first number to |1> using CNOT gate
for i in range(l2):
    if n2[i] == "1":
        qc.x(b[l2-(i+1)])                           #Changing all qubits corresponding to 1 in the second number to |1> using CNOT gate
for i in range(n-1):
    qc.ccx(a[i],b[i],c[i+1])                        #Applying CCNOT gate with current qubits of the two numbers as control and changes the next carry bit
    qc.cx(a[i],b[i])                                #Applying CNOT gate with the qubits of first number as control and make changes to the qubits of the second number
    qc.ccx(c[i],b[i],c[i+1])                        #Applying CCNOT gate with the current carry bit and current qubit of the second number as control and make changes to the next carry bit
qc.ccx(a[n-1],b[n-1],b[n])                          #Making changes corresponding to the final carry bits 
qc.cx(a[n-1],b[n-1])
qc.ccx(c[n-1],b[n-1],b[n])
qc.cx(c[n-1],b[n-1])
for i in range(n-1):                                #Reversing the qubits
    qc.ccx(c[(n-2)-i],b[(n-2)-i],c[(n-1)-i])
    qc.cx(a[(n-2)-i],b[(n-2)-i])
    qc.ccx(a[(n-2)-i],b[(n-2)-i],c[(n-1)-i])
    qc.cx(c[(n-2)-i],b[(n-2)-i])
    qc.cx(a[(n-2)-i],b[(n-2)-i])
for i in range(n+1):
    qc.measure(b[i],cl[i])                          #Measuring thre qubits and storing its values to a classical register
print(qc)                                           #Printing the quantum circuit using ASCII characters
backend = BasicAer.get_backend('qasm_simulator')    #Creating a backend using virtual qasm simulator
job = execute(qc, backend, shots=2)                 #Creating a job
counts = job.result().get_counts(qc)                #Calculating the occurances of each output
print(counts)
