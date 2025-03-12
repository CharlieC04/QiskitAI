from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit.circuit import IfElseOp
def create_conditional_circuit():
    """ Create a one-qubit quantum circuit, apply a Hadamard gate, and then measure it. Based on the classical output, use an IfElseOp operation: if the output is 1, append a one-qubit quantum circuit with a Z gate; if the output is 0, append a one-qubit quantum circuit with an X gate. Finally, add a measurement to the appended circuit and return the complete quantum circuit.
    """
    qr = QuantumRegister(1)
    cr = ClassicalRegister(1)
    qc = QuantumCircuit(qr, cr)
    qc.h(qr[0])
    qc.measure(qr, cr)
    qc.append(IfElseOp(cr[0]), [qr])
    return qc

qc = create_conditional_circuit()
qc.draw()

from qiskit import execute, Aer
backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend, shots=1000)
result = job.result()
counts = result.get_counts()
print(counts)

from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit.circuit import IfElseOp
def create_conditional_circuit():
    """ Create a one-qubit quantum circuit, apply a Hadamard gate, and then measure it. Based on the classical output, use an IfElseOp operation: if the output is 1, append a one-qubit quantum circuit with a Z gate; if the output is 0, append a one