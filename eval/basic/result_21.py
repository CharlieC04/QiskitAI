from qiskit import QuantumCircuit
from qiskit_ibm_runtime.fake_provider import FakeOslo
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
def transpile_circuit_dense() -> QuantumCircuit:
    """ Using a pass manager with optimization level as 1 and dense layout method, transpile and map a bell circuit for the Fake Oslo backend.
    """
    circuit = QuantumCircuit(2)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.measure_all()
    pass_manager = generate_preset_pass_manager("optimization_level=1", backend=FakeOslo())
    transpiled_circuit = pass_manager.run(circuit)
    return transpiled_circuit

transpile_circuit_dense()