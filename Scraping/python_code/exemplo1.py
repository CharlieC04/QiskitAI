from qiskit.providers.aer import QasmSimulator
from multiprocessing import Barrier
from qiskit import*
from qiskit import circuit
import matplotlib.pyplot as plt
from qiskit.tools.visualization import plot_histogram
from qiskit.tools.monitor import job_monitor

circuit = QuantumCircuit(2,2)
circuit.h([0,1])
circuit.barrier()
circuit.cx(0,1)
circuit.measure([0,1],[0,1])


result = execute(circuit, backend= QasmSimulator()).result()
counts = result.get_counts(circuit)


IBMQ.load_account()
host = IBMQ.get_provider('ibm-q')
quantum_computer = host.get_backend('ibmq_belem')
result_qcomputer = execute(circuit, backend= quantum_computer)
print(result_qcomputer.job_id())
job_monitor(result_qcomputer)

result = result_qcomputer.result()

plot_histogram(result.get_counts(circuit))
plt.ylabel(counts)
plt.show()

