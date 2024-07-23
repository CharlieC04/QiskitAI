from qiskit import Aer, IBMQ, execute
from qiskit import transpile, assemble
from qiskit.tools.monitor import job_monitor
from qiskit.tools.monitor import job_monitor
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram, plot_state_city

"""
Qiskit backends to execute the quantum circuit
"""


def simulator(qc):
    """
    Run on local simulator
    :param qc: quantum circuit
    :return:
    """
    backend = Aer.get_backend("qasm_simulator")
    shots = 2048

    tqc = transpile(qc, backend)
    qobj = assemble(tqc, shots=shots)
    job_sim = backend.run(qobj)
    qc_results = job_sim.result()
    return qc_results, shots


def simulator_state_vector(qc):
    """
    Select the StatevectorSimulator from the Aer provider
    :param qc: quantum circuit
    :return:
        statevector
    """
    simulator = Aer.get_backend('statevector_simulator')

    # Execute and get counts
    result = execute(qc, simulator).result()
    state_vector = result.get_statevector(qc)
    return state_vector


def real_quantum_device(qc):
    """
    Use the IBMQ essex device
    :param qc: quantum circuit
    :return:
    """
    provider = IBMQ.load_account()
    backend = provider.get_backend('ibmq_santiago')
    shots = 2048

    TQC = transpile(qc, backend)
    qobj = assemble(TQC, shots=shots)
    job_exp = backend.run(qobj)
    job_monitor(job_exp)
    QC_results = job_exp.result()
    return QC_results, shots


def counts(qc_results):
    """
    Get counts representing the wave-function amplitudes
    :param qc_results:
    :return: dict keys are bit_strings and their counting values
    """
    return qc_results.get_counts()


def plot_results(qc_results):
    """
    Visualizing wave-function amplitudes in a histogram
    :param qc_results: quantum circuit
    :return:
    """
    plt.show(plot_histogram(qc_results.get_counts(), figsize=(8, 6), bar_labels=False))


def plot_state_vector(state_vector):
    """Visualizing state vector in the density matrix representation"""
    plt.show(plot_state_city(state_vector))
