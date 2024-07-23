import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit.providers.fake_provider import FakeAuckland
backend = FakeAuckland()

ghz = QuantumCircuit(15)
ghz.h(0)
ghz.cx(0, range(1, 15))

depths = []
gate_counts = []
non_local_gate_counts = []
levels = [str(x) for x in range(4)]
for level in range(4):
     circ = transpile(ghz, backend, optimization_level=level)
     depths.append(circ.depth())
     gate_counts.append(sum(circ.count_ops().values()))
     non_local_gate_counts.append(circ.num_nonlocal_gates())
fig, (ax1, ax2) = plt.subplots(2, 1)
ax1.bar(levels, depths, label='Depth')
ax1.set_xlabel("Optimization Level")
ax1.set_ylabel("Depth")
ax1.set_title("Output Circuit Depth")
ax2.bar(levels, gate_counts, label='Number of Circuit Operations')
ax2.bar(levels, non_local_gate_counts, label='Number of non-local gates')
ax2.set_xlabel("Optimization Level")
ax2.set_ylabel("Number of gates")
ax2.legend()
ax2.set_title("Number of output circuit gates")
fig.tight_layout()
plt.show()