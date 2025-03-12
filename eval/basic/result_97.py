from qiskit_ibm_runtime.fake_provider.fake_backend import FakeBackendV2
from qiskit_ibm_runtime import IBMBackend
from typing import Union
def two_qubit_conections(
    backend: Union[FakeBackendV2, IBMBackend]
) -> list:
    """ Return the two qubit connections for any input backend of type FakeBackendV2, IBMBackend.
    """
    if isinstance(backend, FakeBackendV2):
        return backend.configuration().coupling_map
    elif isinstance(backend, IBMBackend):
        return backend.configuration().coupling_map
    else:
        raise TypeError(
            f"Backend type {type(backend)} is not supported. "
            "Please use a FakeBackendV2 or IBMBackend."
        )