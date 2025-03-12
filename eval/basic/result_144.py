from qiskit.quantum_info import random_density_matrix, concurrence, DensityMatrix
def concurrence_dataset():
    """ Return a list of 10 density matrices whose concurrence is 0.
    """
    dataset = []
    for i in range(10):
        dataset.append(random_density_matrix(2))
    return dataset

dataset = concurrence_dataset()

for i in range(10):
    print(concurrence(dataset[i]))

# +
from qiskit.quantum_info import random_density_matrix, concurrence, DensityMatrix
def concurrence_dataset():
    """ Return a list of 10 density matrices whose concurrence is 0.
    """
    dataset = []
    for i in range(10):
        dataset.append(random_density_matrix(2))
    return dataset

dataset = concurrence_dataset()

for i in range(10):
    print(concurrence(dataset[i]))

# +
from qiskit.quantum_info import random_density_matrix, concurrence, DensityMatrix
def concurrence_dataset():
    """ Return a list of 10 density matrices whose concurrence is 0.
    """
    dataset = []
    for i in range(10):
        dataset.append(random_density_matrix(2))
    return dataset

dataset = conc