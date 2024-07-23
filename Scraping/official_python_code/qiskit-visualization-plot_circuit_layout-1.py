import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.providers.fake_provider import FakeVigoV2
from qiskit.visualization import plot_circuit_layout
from qiskit.tools.monitor import job_monitor
from qiskit.providers.fake_provider import FakeVigoV2
import matplotlib.pyplot as plt

ghz = QuantumCircuit(3, 3)
ghz.h(0)
for idx in range(1,3):
    ghz.cx(0,idx)
ghz.measure(range(3), range(3))

backend = FakeVigoV2()
new_circ_lv3 = transpile(ghz, backend=backend, optimization_level=3)
plot_circuit_layout(new_circ_lv3, backend)