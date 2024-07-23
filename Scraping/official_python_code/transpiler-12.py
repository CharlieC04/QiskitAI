import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit.providers.fake_provider import FakeAuckland
backend = FakeAuckland()

ghz = QuantumCircuit(15)
ghz.h(0)
ghz.cx(0, range(1, 15))

depths = []
for _ in range(100):
    depths.append(
        transpile(
            ghz,
            backend,
            layout_method='trivial'  # Fixed layout mapped in circuit order
        ).depth()
    )

plt.figure(figsize=(8, 6))
plt.hist(depths, align='left', color='#AC557C')
plt.xlabel('Depth', fontsize=14)
plt.ylabel('Counts', fontsize=14);