from qiskit.visualization import plot_error_map
from qiskit_ibm_runtime.fake_provider import FakeBelemV2
def backend_error_map():
    """ Instantiate a FakeBelemV2 backend and return the plot of its error_map.
    """
    backend = FakeBelemV2()
    plot_error_map(backend.error_map())
backend_error_map()