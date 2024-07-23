from qiskit import ClassicalRegister, QuantumRegister
from qiskit import QuantumCircuit, execute
from qiskit.tools.visualization import plot_histogram, circuit_drawer

q = QuantumRegister(2)
c = ClassicalRegister(2)
#quantum circuit is used to perform operations on qubits
qc = QuantumCircuit(q, c)
#hadamard gate (ususally used to create superposition)
qc.h(q[0])
#controllled not gate
qc.cx(q[0], q[1])
#measures the qubits
qc.measure(q, c)
#run simulation (default backend: "local_qasm_simulator")
job_sim = execute(qc, "local_qasm_simulator")
#Simulation Results
sim_result = job_sim.result()
#qubit probability results
print(sim_result.get_counts(qc))
#visualize simulation results in histogram
plot_histogram(sim_result.get_counts(qc))