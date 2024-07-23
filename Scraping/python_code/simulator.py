from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_histogram


# simulate in statevector_simulator
def simulateStatevector(circuit):
    backend = Aer.get_backend('statevector_simulator')
    result = execute(circuit.remove_final_measurements(inplace=False), backend, shots=1).result()
    counts = result.get_counts()
    return result.get_statevector(circuit)
    # return plot_histogram(counts, color='midnightblue', title="StateVector Histogram")


# simulate in qasm_simulator
def simulateQasm(circuit, count=1024):
    backend = Aer.get_backend('qasm_simulator')
    result = execute(circuit, backend, shots=count).result()
    counts = result.get_counts()
    return plot_histogram(counts, color='midnightblue', title="Qasm Histogram")
