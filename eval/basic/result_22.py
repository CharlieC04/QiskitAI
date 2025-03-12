from qiskit import QuantumCircuit
from qiskit_ibm_runtime.fake_provider import FakeAuckland
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
def transpile_circuit_alap() -> QuantumCircuit:
    """ Using a pass manager with optimization level as 1 and as-late-as-possible scheduling method, transpile and map a bell circuit for the Fake Auckland backend. Return the circuit.
    """
    backend = FakeAuckland()
    pass_manager = generate_preset_pass_manager(backend, optimization_level=1, as_late_as_possible=True)
    circuit = QuantumCircuit(2, 2)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.measure([0, 1], [0, 1])
    circuit = pass_manager.run(circuit)
    return circuit

transpile_circuit_alap()