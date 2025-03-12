from qiskit_aer.noise import NoiseModel, ReadoutError
def noise_model_with_readouterror():
    """ Construct a noise model with specific readout error properties for different qubits. For qubit 0, a readout of 1 has a 20% probability 
    of being erroneously read as 0, and a readout of 0 has a 30% probability of being erroneously read as 1. For all other qubits, a readout of 1 has a 3% 
    probability of being erroneously read as 0, and a readout of 0 has a 2% probability of being erroneously read as 1.
    """
    noise_model = NoiseModel()
    noise_model.add_all_qubit_quantum_error(readout_error(0.2, 0.3), 'id')
    noise_model.add_all_qubit_quantum_error(readout_error(0.03, 0.02), 'x')
    return noise_model

def readout_error(prob_0, prob_1):
    """ Construct a readout error channel for a qubit. The probability of a readout of 0 is prob_0, and the probability of a readout of 1 is prob_1.
    """
    error_channel = ReadoutError([prob_0, prob_1])
    return error_channel

noise_model = noise_model_with_readouterror()

# +
from qiskit_aer.noise import NoiseModel, QuantumError, ReadoutError

def noise_model_with_readouterror():
    """ Construct a noise model with specific readout error properties for different qubits. For qubit 0, a readout of 1 has a 20% probability 
    of