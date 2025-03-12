from qiskit_ibm_runtime.fake_provider import FakeCairoV2
from qiskit_aer.noise import NoiseModel
def gen_noise_model():
    """ Generate a noise model from the Fake Cairo V2 backend.
    """
    backend = FakeCairoV2()
    noise_model = NoiseModel.from_backend(backend)
    return noise_model

noise_model = gen_noise_model()

# +
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_ibm_runtime.exceptions import QiskitRuntimeServiceError

service = QiskitRuntimeService()
try:
    service.get_credentials()
except QiskitRuntimeServiceError as e:
    print(e)

# +
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_ibm_runtime import Sampler
from qiskit_ibm_runtime.exceptions import QiskitRuntimeServiceError

service = QiskitRuntimeService()
try:
    service.get_credentials()
except QiskitRuntimeServiceError as e:
    print(e)

sampler = Sampler(service=service, noise_model=noise_model)

# +
from qiskit.circuit.library import RealAmplitudes

ansatz = RealAmplitudes(num_qubits=4, reps=1)