from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit, execute, Aer

# https://quantum-circuit.com/app_details/about/66bpe6Jf5mgQMahgd
# oracle = '(A | B) & (A | ~B) & (~A | B)'

qc = QuantumCircuit()

q = QuantumRegister(8, 'q')
c = ClassicalRegister(2, 'c')

qc.add_register(q)
qc.add_register(c)

qc.h(q[0])
qc.h(q[1])
qc.x(q[2])
qc.x(q[3])
qc.x(q[4])
qc.x(q[7])
qc.x(q[0])
qc.x(q[1])
qc.h(q[7])
qc.ccx(q[0], q[1], q[2])
qc.x(q[0])
qc.x(q[1])
qc.x(q[1])
qc.ccx(q[0], q[1], q[3])
qc.x(q[0])
qc.x(q[1])
qc.ccx(q[1], q[0], q[4])
qc.x(q[0])
qc.ccx(q[3], q[2], q[5])
qc.x(q[0])
qc.ccx(q[5], q[4], q[6])
qc.cx(q[6], q[7])
qc.ccx(q[4], q[5], q[6])
qc.ccx(q[2], q[3], q[5])
qc.x(q[4])
qc.ccx(q[0], q[1], q[4])
qc.x(q[0])
qc.x(q[1])
qc.x(q[3])
qc.ccx(q[0], q[1], q[3])
qc.x(q[0])
qc.x(q[1])
qc.x(q[2])
qc.x(q[1])
qc.ccx(q[0], q[1], q[2])
qc.x(q[0])
qc.x(q[1])
qc.h(q[0])
qc.h(q[1])
qc.x(q[0])
qc.x(q[1])
qc.cz(q[0], q[1])
qc.x(q[0])
qc.x(q[1])
qc.h(q[0])
qc.h(q[1])
qc.measure(q[0], c[0])
qc.measure(q[1], c[1])


def get_circuit(**kwargs):
    return qc
