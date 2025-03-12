from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
def create_uniform_superposition(n: int) -> QuantumCircuit:
    """ Initialize a uniform superposition on n qubits and return statevector.
    """
    qc = QuantumCircuit(n)
    for i in range(n):
        qc.h(i)
    return qc

qc = create_uniform_superposition(3)
qc.draw()

sv = Statevector.from_instruction(qc)
sv.draw()

sv.data

sv.probabilities()

sv.draw('text')

sv.draw('latex')

sv.draw('mpl')

sv.draw('latex_source')

sv.draw('latex_source')

sv.draw('latex_source')

sv.draw('latex_source')

sv.draw('latex_source')

sv.draw('latex_source')

sv.draw('latex_source')

sv.draw('latex_source')

sv.draw('latex_source')

sv.draw('latex_source')

sv.draw('latex_source')

sv.draw('latex_source')

sv.draw('latex_source')

sv.draw('latex_source')

sv.draw('latex_source')

sv.