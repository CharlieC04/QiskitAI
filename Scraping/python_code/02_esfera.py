import qiskit as q
from qiskit.visualization import plot_histogram, plot_bloch_multivector
import math

qasm_sim = q.Aer.get_backend('qasm_simulator')
statevec_sim = q.Aer.get_backend("statevector_simulator")

c = q.QuantumCircuit(2,2)
c.ry(math.pi/4,0)
c.ry(math.pi/4,1)

orig_statevec = q.execute(c, backend=statevec_sim).result().get_statevector()
c.measure([0,1], [0,1]) # measuring qubit 3, which is impacted by those cnots:

orig_counts = q.execute(c, backend=qasm_sim, shots=1024).result().get_counts()
plot_bloch_multivector(orig_statevec)