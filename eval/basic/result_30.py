from qiskit import QuantumCircuit
from matplotlib.figure import Figure
from qiskit.visualization import plot_state_city
from qiskit.quantum_info import Statevector
def plot_circuit_layout_bell() -> Figure:
    """ Plot a city_state for a bell circuit.
    """
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    return plot_state_city(Statevector.from_instruction(qc))

plot_circuit_layout_bell()