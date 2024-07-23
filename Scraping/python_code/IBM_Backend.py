from qiskit.providers.ibmq import least_busy
from qiskit import IBMQ
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute

#IBMQ.save_account("Account id")
APItoken="APItoken"                
config = { "url": 'https://quantumexperience.ng.bluemix.net/api'}
#IBMQ.backends()
#Search for available quantum machines 
IBMQ.load_accounts()
print("Available backends")
print(IBMQ.backends())

large_enough_devices = IBMQ.backends(filters=lambda x : x.configuration().n_qubits >3 and not x.configuration().simulator)
backend = least_busy(large_enough_devices)
print(backend)
print("The best backend is "+ backend.name())
#Creating quantum circuits
q = QuantumRegister(2)
c = ClassicalRegister(2)
qc = QuantumCircuit(q,c)
m = QuantumCircuit(q,c)
qc.h(q)
qc.cx(q[0],q[1])
m.measure(q,c)
t = qc + m
#Executing the quantum circuits in a real quantum computer
job = execute(t,backend,shots=1000)
counts = job.result().get_counts(t)
print(counts)
