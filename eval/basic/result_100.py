from qiskit.transpiler.passes import SolovayKitaev
from qiskit.transpiler import PassManager
from qiskit.circuit import QuantumCircuit
def sol_kit_decomp(circuit: QuantumCircuit) -> QuantumCircuit:
    """ Create a pass manager to decompose the single qubit gates into gates of the dense subset ['t', 'tdg', 'h'] in the given circuit.
    """
    return PassManager(
        [
            SolovayKitaev(num_qubits=circuit.num_qubits, seed=12345),
        ]
    )

circuit = QuantumCircuit(2)
circuit.h(0)
circuit.cx(0, 1)
circuit.h(1)
circuit.cx(0, 1)
circuit.h(0)
circuit.cx(0, 1)
circuit.h(1)
circuit.cx(0, 1)
circuit.h(0)
circuit.cx(0, 1)
circuit.h(1)
circuit.cx(0, 1)
circuit.h(0)
circuit.cx(0, 1)
circuit.h(1)
circuit.cx(0, 1)
circuit.h(0)
circuit.cx(0, 1)
circuit.h(1)
circuit.cx(0, 1)
circuit.h(0)
circuit.cx(0, 1)
circuit.h(1)
circuit.cx(0, 1)
circuit.