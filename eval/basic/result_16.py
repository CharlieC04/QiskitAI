from qiskit_ibm_runtime.fake_provider import FakeCairoV2
from qiskit.transpiler import CouplingMap
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
def transpile_circuit(circuit: QuantumCircuit) -> QuantumCircuit:
    """ For the given Quantum Circuit, return the transpiled circuit for the Fake Cairo V2 backend using pass manager with optimization level as 1.
    """
    coupling_map = CouplingMap.from_line(2)
    pass_manager = generate_preset_pass_manager("optimization_level 1", backend=FakeCairoV2(), coupling_map=coupling_map)
    transpiled_circuit = pass_manager.run(circuit)
    return transpiled_circuit

circuit = QuantumCircuit(2)
circuit.h(0)
circuit.cx(0, 1)
circuit.measure_all()
transpiled_circuit = transpile_circuit(circuit)
transpiled_circuit.draw()