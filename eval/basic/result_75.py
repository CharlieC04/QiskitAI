from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
def circuit_to_bools(circuit: QuantumCircuit) -> list[bool]:
    """ Given a QuantumCircuit, sample it once and convert the measurement result to a list of bools, where the 0th bool is the result of the 0th classical bit.
    """
    sampler = StatevectorSampler()
    result = sampler.run(circuit).result()
    statevector = result.get_statevector(circuit)
    return [bool(int(bit)) for bit in statevector]

circuit = QuantumCircuit(1)
circuit.x(0)
circuit.measure_all()
circuit_to_bools(circuit)

circuit = QuantumCircuit(1)
circuit.measure_all()
circuit_to_bools(circuit)

circuit = QuantumCircuit(1)
circuit.x(0)
circuit.measure_all()
circuit_to_bools(circuit)

circuit = QuantumCircuit(1)
circuit.measure_all()
circuit_to_bools(circuit)

circuit = QuantumCircuit(1)
circuit.x(0)
circuit.measure_all()
circuit_to_bools(circuit)

circuit = QuantumCircuit(1)
circuit.measure_all()
circuit_to_bools(circuit)

circuit = QuantumCircuit(1)
circuit.x(0)
circuit.measure_all()
circuit_