from qiskit import *


def random_int(backend, size):
    circuit = QuantumCircuit.from_qasm_file("Random_number.qasm")

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
