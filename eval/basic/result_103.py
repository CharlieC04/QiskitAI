import importlib
import inspect
from qiskit_ibm_runtime.fake_provider import fake_backend
def fake_providers_v2_with_ecr() -> list:
    """ Return the list of names of all the fake providers of type FakeBackendV2 which contains ecr gates in its available operations.
    """
    fake_providers = []
    for name, obj in inspect.getmembers(importlib.import_module("qiskit_ibm_runtime.fake_provider")):
        if inspect.isclass(obj) and issubclass(obj, fake_backend.FakeBackendV2) and "ecr" in obj.available_operations():
            fake_providers.append(name)
    return fake_providers

def fake_providers_v2_without_ecr() -> list:
    """ Return the list of names of all the fake providers of type FakeBackendV2 which does not contain ecr gates in its available operations.
    """
    fake_providers = []
    for name, obj in inspect.getmembers(importlib.import_module("qiskit_ibm_runtime.fake_provider")):
        if inspect.isclass(obj) and issubclass(obj, fake_backend.FakeBackendV2) and "ecr" not in obj.available_operations():
            fake_providers.append(name)
    return fake_providers

def fake_providers_v1() -> list:
    """ Return the list of names of all the fake providers of type FakeBackendV