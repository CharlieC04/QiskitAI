from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler
def random_coin_flip(samples: int)->dict:
    """ Design a Quantum Circuit that simulates random coin flips for the given samples using Qiskit Sampler with the Aer simulator as backend and outputs the count of heads and tails in a dictionary. The heads should be stored in the dict as 'Heads' and tails as 'Tails'. For example
    random_coin_flip(10) == {'Heads' : 5, 'Tails : 5}
    random_coin_flip(20) == {'Heads' : 9, 'Tails : 11}.
    """
    # YOUR CODE HERE
    qc = QuantumCircuit(1)
    qc.h(0)
    qc.measure_all()
    backend = AerSimulator()
    sampler = Sampler(backend)
    result = sampler.run(qc, shots=samples).result()
    counts = result.get_counts()
    return {'Heads': counts['1'], 'Tails': counts['0']}