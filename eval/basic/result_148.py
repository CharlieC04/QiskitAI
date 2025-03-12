from qiskit import QuantumCircuit
from qiskit.transpiler.passes import BasicSwap
from qiskit.converters import circuit_to_dag, dag_to_circuit
from qiskit_ibm_runtime import IBMBackend
def swap_map(qc: QuantumCircuit, backend: IBMBackend) -> QuantumCircuit:
    """ Add SWAPs to route `qc` for the `backend` object's coupling map, but don't transform any gates.
    """
    dag = circuit_to_dag(qc)
    dag = BasicSwap(backend.coupling_map).run(dag)
    return dag_to_circuit(dag)

qc = QuantumCircuit(2)
qc.cx(0, 1)
qc.draw()

swap_map(qc, backend).draw()

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.draw()

swap_map(qc, backend).draw()

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.h(0)
qc.draw()

swap_map(qc, backend).draw()

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.h(0)
qc.cx(0, 1)
qc.draw()

swap_map(qc, backend).draw()

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 