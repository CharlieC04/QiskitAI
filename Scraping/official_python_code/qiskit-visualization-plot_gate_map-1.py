from qiskit import QuantumCircuit, execute
from qiskit.providers.fake_provider import FakeVigoV2
from qiskit.visualization import plot_gate_map

backend = FakeVigoV2()

plot_gate_map(backend)