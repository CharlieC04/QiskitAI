from qiskit import QuantumCircuit, execute
from qiskit.visualization import plot_error_map
from qiskit.providers.fake_provider import FakeVigoV2

backend = FakeVigoV2()
plot_error_map(backend)