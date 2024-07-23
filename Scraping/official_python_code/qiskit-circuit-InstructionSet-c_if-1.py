from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit

qr = QuantumRegister(2)
cr = ClassicalRegister(2)
qc = QuantumCircuit(qr, cr)
qc.h(range(2))
qc.measure(range(2), range(2))

# apply x gate if the classical register has the value 2 (10 in binary)
qc.x(0).c_if(cr, 2)

# apply y gate if bit 0 is set to 1
qc.y(1).c_if(0, 1)

qc.draw('mpl')