from qiskit import IBMQ
from qiskit import *

#provider = IBMQ.enable_account(<INSERT_IBM_QUANTUM_EXPERIENCE_TOKEN>)

qc = QuantumCircuit(2,2)
qc.h(0)
qc.cx(0,1)
qc.measure(1,0)
backend = IBMQ.get_backend('ibmq_qasm_simulator', hub=None)
job=execute(qc, backend, shots=1000)

result = job.result()
print(result.get_counts())