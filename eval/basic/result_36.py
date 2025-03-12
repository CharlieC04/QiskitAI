from qiskit import QuantumCircuit
def bv_function(s: str) -> QuantumCircuit:
    """ Write a function to design a Bernstein-Vazirani oracle from a bitstring and return it.
    """
    n = len(s)
    qc = QuantumCircuit(n+1)
    qc.x(n)
    qc.h(range(n+1))
    for i in range(n):
        if s[i] == '1':
            qc.cx(i, n)
    qc.h(range(n+1))
    return qc
bv_function('101').draw('mpl')

from qiskit import QuantumCircuit
def bv_function(s: str) -> QuantumCircuit:
    """ Write a function to design a Bernstein-Vazirani oracle from a bitstring and return it.
    """
    n = len(s)
    qc = QuantumCircuit(n+1)
    qc.x(n)
    qc.h(range(n+1))
    for i in range(n):
        if s[i] == '1':
            qc.cx(i, n)
    qc.h(range(n+1))
    return qc
bv_function('101').draw('mpl')

from qiskit import QuantumCircuit
def