from qiskit import QuantumCircuit, transpile, schedule
from qiskit.visualization.pulse_v2 import draw, IQXSimple
from qiskit.providers.fake_provider import FakeBoeblingen

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()
qc = transpile(qc, FakeBoeblingen(), layout_method='trivial')
sched = schedule(qc, FakeBoeblingen())

draw(sched, style=IQXSimple(), backend=FakeBoeblingen())