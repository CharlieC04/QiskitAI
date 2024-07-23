from qiskit import BasicAer, transpile, QuantumRegister, ClassicalRegister, QuantumCircuit

qr = QuantumRegister(1)
cr = ClassicalRegister(1)
qc = QuantumCircuit(qr, cr)
qc.h(0)
qc.measure(0, 0)
qc.draw('mpl')