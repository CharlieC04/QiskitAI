from qiskit import QuantumRegister
from qiskit.transpiler.basepasses import TransformationPass
from qiskit.dagcircuit import DAGCircuit
from qiskit.circuit.library import ZGate, HGate, XGate
def create_hxh_pass() -> TransformationPass:
    """ Return a transpiler pass that replaces all non-controlled Z-gates with H-X-H-gate sequences.
    """
    class HXHPass(TransformationPass):
        def run(self, dag: DAGCircuit) -> DAGCircuit:
            """ Replace all non-controlled Z-gates with H-X-H-gate sequences.
            """
            for node in dag.nodes():
                if isinstance(node.op, ZGate) and not node.control_qubits:
                    # Replace Z-gate with H-X-H-gate sequence
                    h_node = dag.apply_operation_back(HGate(), [node.qargs[0]])
                    x_node = dag.apply_operation_back(XGate(), [node.qargs[0]])
                    h_node = dag.apply_operation_back(HGate(), [node.qargs[0]])
                    dag.remove_op_node(node)
                    dag.add_op_node(h_node)
                    dag.add_op_node(x_node)
                    dag.add_op_node(h_node)
            return dag
    return HXHPass()

qr = QuantumRegister(2)
dag = DAGCircuit(qr)
dag.append(ZGate(), [qr[0]])
dag.append