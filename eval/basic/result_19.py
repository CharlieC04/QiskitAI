from qiskit import QuantumCircuit
from qiskit_ibm_runtime.fake_provider import FakeTorontoV2
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
def transpile_circuit_maxopt() -> QuantumCircuit:
    """ Transpile and map an 11-qubit GHZ circuit for the Fake Toronto V2 backend using pass manager with maximum transpiler optimization.
    """
    circuit = QuantumCircuit(11)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.cx(0, 2)
    circuit.cx(0, 3)
    circuit.cx(0, 4)
    circuit.cx(0, 5)
    circuit.cx(0, 6)
    circuit.cx(0, 7)
    circuit.cx(0, 8)
    circuit.cx(0, 9)
    circuit.cx(0, 10)
    circuit.measure_all()
    backend = FakeTorontoV2()
    pass_manager = generate_preset_pass_manager(backend, optimization_level=3)
    transpiled_circuit = pass_manager.run(circuit)
    return transpiled_circuit

transpiled_circuit = transpile_circuit_maxopt()
transpiled_circuit.draw()