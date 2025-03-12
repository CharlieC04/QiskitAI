from matplotlib.figure import Figure
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler
from qiskit.visualization import plot_histogram
def visualize_bell_states()->Figure:
    """ Prepare phi plus and phi minus bell states and visualize their results in a histogram and return the histogram.
    """
    # Prepare the quantum circuit
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    # Simulate the circuit
    backend = AerSimulator()
    job = backend.run(qc)
    result = job.result()
    counts = result.get_counts()
    # Visualize the results
    fig = plot_histogram(counts)
    return fig

visualize_bell_states()

def visualize_bell_states_with_measurement()->Figure:
    """ Prepare phi plus and phi minus bell states and visualize their results in a histogram and return the histogram.
    """
    # Prepare the quantum circuit
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    # Simulate the circuit
    backend = AerSimulator()
    job = backend.run(qc)
    result = job.result()
    counts = result.get_counts()
    # Visualize the results
    fig = plot_histogram(counts)
    return fig

visualize_bell_states_with_measurement()

def visualize