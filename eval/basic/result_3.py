from qiskit import QuantumCircuit
def create_ghz(drawing=False):
    """ Generate a QuantumCircuit for a 3 qubit GHZ State and measure it. If `drawing` is True, return both the circuit object and the Matplotlib drawing of the circuit, otherwise return just the circuit object.
    """
    qc = QuantumCircuit(3)
    qc.h(0)
    qc.cx(0,1)
    qc.cx(0,2)
    qc.measure_all()
    if drawing:
        return qc, qc.draw('mpl')
    else:
        return qc
qc = create_ghz(drawing=True)
qc.draw('mpl')
from qiskit import Aer
backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend, shots=1000)
result = job.result()
counts = result.get_counts()
print(counts)
from qiskit.visualization import plot_histogram
plot_histogram(counts)

qc = create_ghz()
qc.draw('mpl')
from qiskit import IBMQ
IBMQ.save_account('YOUR_API_TOKEN')
IBMQ.load_account()
provider = IBMQ.get_provider(hub='ibm-q')
provider.backends()
backend = provider.get_backend('ibmq_qasm_simulator')
job = execute(