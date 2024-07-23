from qiskit import QuantumCircuit, transpile, schedule
from qiskit.visualization.timeline import draw, IQXSimple
from qiskit.providers.fake_provider import FakeBoeblingen

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0,1)

qc = transpile(qc, FakeBoeblingen(), scheduling_method='alap', layout_method='trivial')
draw(qc, style=IQXSimple())