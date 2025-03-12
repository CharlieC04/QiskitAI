from qiskit.circuit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit.classical import expr
def conditional_quantum_circuit():
    """ Create a quantum circuit with 4 qubits and 4 classical bits. Apply Hadamard gates to the first three qubits, measure them with three classical registers,
    and conditionally apply an X gate to the fourth qubit based on the XOR of the three classical bits. Finally, measure the fourth qubit into another classical register.
    """
    qr = QuantumRegister(4, 'q')
    cr = ClassicalRegister(4, 'c')
    qc = QuantumCircuit(qr, cr)
    qc.h(qr[0:3])
    qc.measure(qr[0:3], cr[0:3])
    qc.x(qr[3]).c_if(cr[0:3], 1)
    qc.measure(qr[3], cr[3])
    return qc

qc = conditional_quantum_circuit()
qc.draw('mpl')

from qiskit.providers.aer import AerSimulator
from qiskit.visualization import plot_histogram

backend = AerSimulator()
job = backend.run(qc)
result = job.result()
counts = result.get_counts()
plot_histogram(counts)

from qiskit.providers.aer import AerSimulator
from qiskit.visualization import plot_histogram

backend = AerSimulator()
job = backend.run(qc, shots=1000)
result = job.result()
counts = result.get_counts()
