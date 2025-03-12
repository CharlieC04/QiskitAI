from qiskit import QuantumCircuit
from qiskit_ibm_runtime.fake_provider import FakeSydneyV2
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
def transpile_circuit_noopt() -> QuantumCircuit:
    """ Transpile a 10-qubit GHZ circuit for the Fake Sydney V2 backend using pass manager with no optimization.
    """
    circuit = QuantumCircuit(10)
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
    circuit.measure_all()
    return circuit

def transpile_circuit_opt() -> QuantumCircuit:
    """ Transpile a 10-qubit GHZ circuit for the Fake Sydney V2 backend using pass manager with optimization.
    """
    circuit = QuantumCircuit(10)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.cx(0, 2)
    circuit.cx(0, 3)
    circuit.cx(0, 4)
    circuit.cx(0, 5)
    circuit.cx(0, 6)
    circuit.cx(0, 7)
    circuit.cx(