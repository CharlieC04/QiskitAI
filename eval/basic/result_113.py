from qiskit import QuantumCircuit
from qiskit.transpiler import PassManager, PropertySet
from qiskit.transpiler.passes import RemoveBarriers
def calculate_depth_after_barrier_removal(qc: QuantumCircuit) -> PropertySet:
    """ Remove barriers from the given quantum circuit and calculate the depth before and after removal.
    Return a PropertySet with 'depth_before', 'depth_after', and 'width' properties.
    The function should only remove barriers and not perform any other optimizations.
    """
    # Create a PassManager with the RemoveBarriers pass
    pm = PassManager(RemoveBarriers())

    # Apply the pass to the circuit
    pm.run(qc)

    # Calculate the depth of the circuit before and after removing barriers
    depth_before = qc.depth()
    depth_after = pm.property_set.depth

    # Calculate the width of the circuit
    width = qc.width()

    # Create a PropertySet with the calculated depths and width
    properties = PropertySet()
    properties.depth_before = depth_before
    properties.depth_after = depth_after
    properties.width = width

    return properties