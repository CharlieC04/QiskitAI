from qiskit import QuantumCircuit
from qiskit.circuit.library import Barrier
def split_circuit_at_barriers(circuit: QuantumCircuit) -> list[QuantumCircuit]:
    """ Split `circuit` at each barrier operation. Do not include barriers in the output circuits.
    """
    split_circuits = []
    for i in range(len(circuit.data)):
        if circuit.data[i].operation.name == "barrier":
            split_circuits.append(circuit.data[i - 1 : i])
        else:
            split_circuits.append(circuit.data[i : i + 1])
    return split_circuits

circuit = QuantumCircuit(3)
circuit.h(0)
circuit.cx(0, 1)
circuit.cx(1, 2)
circuit.barrier()
circuit.cx(0, 1)
circuit.cx(1, 2)
circuit.barrier()
circuit.cx(0, 1)
circuit.cx(1, 2)

split_circuits = split_circuit_at_barriers(circuit)
for split_circuit in split_circuits:
    print(split_circuit)

from qiskit import QuantumCircuit
from qiskit.circuit.library import Barrier
def split_circuit_at_barriers(circuit: QuantumCircuit) -> list[QuantumCircuit]:
    """ Split `circuit` at