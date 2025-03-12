from qiskit.quantum_info import entropy, random_density_matrix, DensityMatrix
def pure_states(ε):
    """ Return a list of ten density matrices which are pure up to a tolerance of ε.
    """
    return [DensityMatrix(random_density_matrix(2)).unitary() for _ in range(10)]

def mixed_states(ε):
    """ Return a list of ten density matrices which are mixed up to a tolerance of ε.
    """
    return [DensityMatrix(random_density_matrix(2)).mixed() for _ in range(10)]

def mixed_and_pure_states(ε):
    """ Return a list of ten density matrices which are mixed up to a tolerance of ε,
    and pure up to a tolerance of ε.
    """
    return [DensityMatrix(random_density_matrix(2)).mixed() if random.random() < 0.5 else DensityMatrix(random_density_matrix(2)).unitary() for _ in range(10)]

def mixed_and_pure_states_with_different_epsilon(ε1, ε2):
    """ Return a list of ten density matrices which are mixed up to a tolerance of ε1,
    and pure up to a tolerance of ε2.
    """
    return [DensityMatrix(random_density_matrix(2)).mixed() if random.random() < 0.5 else