import numpy as np
from typing import Union
from qiskit_ibm_runtime.fake_provider.fake_backend import FakeBackendV2
from qiskit_ibm_runtime import IBMBackend
def qubit_with_least_readout_error(backend: Union[IBMBackend, FakeBackendV2])-> float:
    """ Return the minimum readout error of any input backend of type FakeBackendV2, IBMBackend.
    """
    if isinstance(backend, FakeBackendV2):
        return backend.properties().readout_error_per_qubit[0]
    elif isinstance(backend, IBMBackend):
        return backend.properties().readout_error_per_qubit[0]
    else:
        raise TypeError("Input backend must be of type FakeBackendV2 or IBMBackend.")

def qubit_with_least_gate_error(backend: Union[IBMBackend, FakeBackendV2])-> float:
    """ Return the minimum gate error of any input backend of type FakeBackendV2, IBMBackend.
    """
    if isinstance(backend, FakeBackendV2):
        return backend.properties().gate_error_per_qubit[0]
    elif isinstance(backend, IBMBackend):
        return backend.properties().gate_error_per_qubit[0]
    else:
        raise TypeError("Input backend must be of type FakeBackendV2 or IBMBackend.")

def qubit_with_least_gate_error_and_readout_error(backend: Union[IBMBackend, FakeBackendV2])-> float:
    """ Return the minimum gate error of any input backend of type FakeBackendV2,