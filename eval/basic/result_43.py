from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit import QuantumCircuit
def generate_pass_manager_obj()-> QuantumCircuit:
    """ Instantiate a preset_passmanager using Qiskit using the least busy device available and optimzation level 3. Return the resulting passmanager instance.
    """
    service = QiskitRuntimeService()
    backend = service.get_backend("ibmq_qasm_simulator")
    pass_manager = generate_preset_pass_manager(backend, optimization_level=3)
    return pass_manager

pass_manager = generate_pass_manager_obj()

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()
qc.draw()

qc_transpiled = pass_manager.run(qc)
qc_transpiled.draw()

qc_transpiled.count_ops()

qc_transpiled.count_ops()

qc_transpiled.count_ops()

qc_transpiled.count_ops()

qc_transpiled.count_ops()

qc_transpiled.count_ops()

qc_transpiled.count_ops()

qc_transpiled.count_ops()

qc_transpiled.count_ops()

qc_transpiled.count_ops()

qc_transpiled.count_ops()

qc_transpiled.