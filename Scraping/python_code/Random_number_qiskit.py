from qiskit import *

def random_int(backend, size):
    qreg = QuantumRegister(1) #Using only one quibt
    creg = ClassicalRegister(1)

    circuit = QuantumCircuit(qreg,creg)
    circuit.reset(qreg) #Reset the qubit to state |0>

    circuit.h(qreg) #Apply Hadamard gate/put qubit into superposition

    circuit.measure(qreg,creg) #Measure

    job = execute(circuit, backend, shots=size, memory=True) 
    result = job.result()
    bin_num = ''.join(result.get_memory())
    return int(bin_num,2)

#QASM Simulator backend:
backend = Aer.get_backend('qasm_simulator')

#Real IBM Quantum Computer backend
#from qiskit.providers.ibmq import least_busy
#provider = IBMQ.load_account()
#backend = least_busy(provider.backends(filters=lambda x: x.configuration().n_qubits >= 3 and 
#                        not x.configuration().simulator and x.status().operational==True))

bits = 64
print("Here you have a random number: ", random_int(backend, bits))
