from qiskit import Aer, execute, QuantumCircuit, visualization
import matplotlib.pyplot as plt


qc = QuantumCircuit.from_qasm_file('Bell test.qasm')
backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend, shots=2048)
result = job.result()

ax1 = qc.draw("mpl")
ax1.suptitle("Bell test circuit")
ax2 = visualization.plot_histogram(result.get_counts(qc))
ax2.suptitle("Results")
plt.show()
