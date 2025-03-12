from qiskit import QuantumCircuit
def count_instructions(circuit: QuantumCircuit) -> int:
    """ Return the total number of instructions in the circuit.
    """
    return len(circuit.data)

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

count_instructions(qc)

qc.draw()

qc.decompose().draw()

count_instructions(qc.decompose())

qc.decompose().decompose().draw()

count_instructions(qc.decompose().decompose())

qc.decompose().decompose().decompose().draw()

count_instructions(qc.decompose().decompose().decompose())

qc.decompose().decompose().decompose().decompose().draw()

count_instructions(qc.decompose().decompose().decompose().decompose())

qc.decompose().decompose().decompose().decompose().decompose().draw()

count_instructions(qc.decompose().decompose().decompose().decompose().decompose())

qc.decompose().decompose().decompose().decompose().decompose().decompose().draw()

count_instructions(qc.decompose().decompose().decompose