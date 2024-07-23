# %% [markdown]
# # 第3章原始程式碼

# %%
#Program 3.1a Apply X-gate to qubit
from qiskit import QuantumCircuit
qc = QuantumCircuit(2)
qc.x(1)
qc.draw('mpl')

# %%
#Program 3.1b Show Bloch sphere of qubit w/wo X-gate
from qiskit.quantum_info import Statevector
state = Statevector.from_instruction(qc)
state.draw('bloch')

# %%
#Program 3.2a Measure state of qubit w/o X-gate
from qiskit import QuantumCircuit,execute
from qiskit.providers.aer import AerSimulator
from qiskit.visualization import plot_histogram
import math
qc = QuantumCircuit(1,1)
qc.initialize([math.sqrt(1/3), math.sqrt(2/3)],0)
qc.measure([0],[0])
print(qc)
sim=AerSimulator()
job=execute(qc, backend=sim, shots=1000)
result=job.result()
counts=result.get_counts(qc)
print("Counts:",counts)
plot_histogram(counts)

# %%
#Program 3.2b Measure state of qubit w/ X-gate
from qiskit import QuantumCircuit,execute
from qiskit.providers.aer import AerSimulator
from qiskit.visualization import plot_histogram
import math
qc = QuantumCircuit(1,1)
qc.initialize([math.sqrt(1/3), math.sqrt(2/3)],0)
qc.x(0)
qc.measure([0],[0])
print(qc)
sim=AerSimulator()
job=execute(qc, backend=sim, shots=1000)
result=job.result()
counts=result.get_counts(qc)
print("Counts:",counts)
plot_histogram(counts)

# %%
#Program 3.3a Apply X-gate and H-gate to qubit
from qiskit import QuantumCircuit
import math
qc = QuantumCircuit(4)
qc.initialize([1/math.sqrt(2), 1/math.sqrt(2)],0)
qc.initialize([1/math.sqrt(2), -1/math.sqrt(2)],1)
qc.h(2)
qc.x(3)
qc.h(3)
qc.draw('mpl')

# %%
#Program 3.3b Show Bloch sphere of qubit w/ X-gate and H-gate
from qiskit.quantum_info import Statevector
state = Statevector.from_instruction(qc)
state.draw('bloch')

# %%
#Program 3.4 Measure state of qubit w/ H-gate
from qiskit import QuantumCircuit,execute
from qiskit.providers.aer import AerSimulator
from qiskit.visualization import plot_histogram
qc = QuantumCircuit(1,1)
qc.h(0)
qc.measure([0],[0])
print("This is |+>:")
print(qc)
sim=AerSimulator()
job=execute(qc, backend=sim, shots=1000)
result=job.result()
counts=result.get_counts(qc)
print("Counts:",counts)
plot_histogram(counts)

# %%
#Program 3.5 Measure state of qubit w/ X-gate and H-gate
from qiskit import QuantumCircuit,execute
from qiskit.providers.aer import AerSimulator
from qiskit.visualization import plot_histogram
qc = QuantumCircuit(1,1)
qc.x(0)
qc.h(0)
qc.measure([0],[0])
print("This is |->:")
print(qc)
sim=AerSimulator()
job=execute(qc, backend=sim, shots=1000)
result=job.result()
counts=result.get_counts(qc)
print("Counts:",counts)
plot_histogram(counts)

# %%
#Program 3.6 Measure state of qubit w/ H-gate
from qiskit import QuantumCircuit,execute
from qiskit.providers.aer import AerSimulator
from qiskit.visualization import plot_histogram
qc = QuantumCircuit(2,2)
qc.h(0)
qc.h(1)
qc.measure([0,1],[0,1])
print("This is |++>:")
print(qc)
sim=AerSimulator()
job=execute(qc, backend=sim, shots=1000)
result=job.result()
counts=result.get_counts(qc)
print("Counts:",counts)
plot_histogram(counts)

# %%
#Program 3.7a Apply X-, Y-, and Z-gate to qubit
from qiskit import QuantumCircuit
qc = QuantumCircuit(3)
qc.x(0)
qc.y(1)
qc.z(2)
qc.draw('mpl')

# %%
#Program 3.7b Show Bloch sphere of qubit w/ X-, Y-, and Z-gate
from qiskit.quantum_info import Statevector
state = Statevector.from_instruction(qc)
state.draw('bloch')

# %%
#Program 3.8a Apply RX-, RY-, and RZ-gate to qubit
from qiskit import QuantumCircuit
import math
qc = QuantumCircuit(3)
qc.rx(math.pi/2, 0)
qc.ry(math.pi/2, 1)
qc.rz(math.pi/2, 2)
qc.draw('mpl')

# %%
#Program 3.8b Show Bloch sphere of qubit w/ RX-, RY-, and RZ-gate
from qiskit.quantum_info import Statevector
state = Statevector.from_instruction(qc)
state.draw('bloch')

# %%
#Program 3.9a Apply RX-, P-, S-, T-gate to qubit
from qiskit import QuantumCircuit
import math
qc = QuantumCircuit(4)
qc.rx(math.pi/2, [0,1,2,3])
qc.p(math.pi/8, 1)
qc.s(2)
qc.t(3)
qc.draw('mpl')

# %%
#Program 3.9b Show Bloch sphere of qubit w/ RX-, P-, S-, and T-gate
from qiskit.quantum_info import Statevector
state = Statevector.from_instruction(qc)
state.draw('bloch')

# %%
#Program 3.10a Apply RX-, I-, and U-gate to qubit
from qiskit import QuantumCircuit
import math
qc = QuantumCircuit(4)
qc.rx(math.pi/2, [0,1,2,3])
qc.i(1)
qc.u(math.pi/2, 0, math.pi, 2)
qc.u(0,0, math.pi/4, 3)
qc.draw('mpl')

# %%
#Program 3.10b Show Bloch sphere of qubit w/ RX-, I-, and U-gate
from qiskit.quantum_info import Statevector
state = Statevector.from_instruction(qc)
state.draw('bloch')


