from qiskit.quantum_info import Choi
import numpy as np
def initialize_adjoint_and_compose(data1: np.ndarray, data2: np.ndarray) -> (Choi, Choi, Choi):
    """ Initialize Choi matrices for the given data1 and data2 as inputs. Compute data1 adjoint, and then return the data1 Choi matrix, its adjoint and the composed choi matrices in order.
    """
    choi_data1 = Choi(data1)
    choi_data1_adjoint = choi_data1.adjoint()
    choi_data2 = Choi(data2)
    choi_composed = choi_data1_adjoint @ choi_data2
    return choi_data1, choi_data1_adjoint, choi_composed

data1 = np.array([[1, 0], [0, 1]])
data2 = np.array([[1, 0], [0, 1]])

choi_data1, choi_data1_adjoint, choi_composed = initialize_adjoint_and_compose(data1, data2)

print(choi_data1)
print(choi_data1_adjoint)
print(choi_composed)

data1 = np.array([[1, 0], [0, 1]])
data2 = np.array([[0, 1], [1, 0]])

choi_data1, choi_data1_adjoint, choi_composed = initialize_ad