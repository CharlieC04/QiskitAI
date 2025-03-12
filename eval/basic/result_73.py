from qiskit import QuantumCircuit
def x_measurement(circuit: QuantumCircuit, qubit: int, clbit: int) -> None:
    """ Add an X-basis measurement on qubit at index `qubit`, storing the result to classical bit `clbit`.
    """
    circuit.h(qubit)
    circuit.measure(qubit, clbit)
