from qiskit_ibm_runtime.fake_provider import FakeCairoV2
def backend_info(backend_name):
    """ Given the fake backend name, retrieve information about the backend's number of qubits, coupling map, and supported instructions using the Qiskit Runtime Fake Provider, 
    and create a dictionary containing the info. The dictionary must have the following keys: 'num_qubits' (the number of qubits), 'coupling_map' 
    (the coupling map of the backend), and'supported_instructions' (the supported instructions of the backend).
    """
    backend = FakeCairoV2(backend_name)
    num_qubits = backend.configuration().n_qubits
    coupling_map = backend.configuration().coupling_map
    supported_instructions = backend.configuration().basis_gates
    backend_info = {'num_qubits': num_qubits, 'coupling_map': coupling_map,'supported_instructions': supported_instructions}
    return backend_info

backend_info('fake_cairo_v2')

# +
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler, Estimator
from qiskit_ibm_runtime.fake_provider import FakeCairoV2

def backend_info(backend_name):
    """ Given the fake backend name, retrieve information about the backend's number of qubits, coupling map, and supported instructions using the Qiskit Runtime Fake Provider, 
    and create a dictionary containing the info. The dictionary must have the following keys: 'num_qubits' (the number of qubits), 'coupling_map' 
    (the coupling map of the backend), and'supported_instructions' (the supported instructions of the backend).