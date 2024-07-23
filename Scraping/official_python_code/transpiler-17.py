from qiskit.visualization.timeline import draw as timeline_draw

from qiskit import QuantumCircuit, transpile
from qiskit.providers.fake_provider import FakeBoeblingen

backend = FakeBoeblingen()

ghz = QuantumCircuit(5)
ghz.h(0)
ghz.cx(0,range(1,5))

circ = transpile(ghz, backend, scheduling_method="asap")

timeline_draw(circ)