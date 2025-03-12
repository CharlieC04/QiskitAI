from qiskit.transpiler import CouplingMap
def create_and_modify_coupling_map() -> CouplingMap:
    """ Create a CouplingMap with a specific coupling list, then modify it by adding an edge and a physical qubit.
    The initial coupling list is [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5]].
    Add an edge (5, 6), and add a physical qubit "7".
    """
    coupling_map = CouplingMap([[0, 1], [1, 2], [2, 3], [3, 4], [4, 5]])
    coupling_map.add_edge(5, 6)
    coupling_map.add_physical_qubit("7")
    return coupling_map

coupling_map = create_and_modify_coupling_map()
print(coupling_map)

# +
from qiskit.transpiler import CouplingMap
def create_and_modify_coupling_map() -> CouplingMap:
    """ Create a CouplingMap with a specific coupling list, then modify it by adding an edge and a physical qubit.
    The initial coupling list is [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5]].
    Add an edge (5, 6), and add a physical qubit "7".
    """
    coupling_map = CouplingMap([[0, 1], [1, 2], [2, 3], [3, 