import contextlib
from qiskit import QuantumCircuit
from qiskit.circuit import Gate
def gate_if_clbits(
    circuit: QuantumCircuit, gate: Gate, qubits: list[int], condition_clbits: list[int]
) -> None:
    """ Apply `gate` to qubits with indices `qubits`, conditioned on all `condition_clbits` being 1.
    """
    with contextlib.suppress(ValueError):
        circuit.append(gate, qubits + condition_clbits)
