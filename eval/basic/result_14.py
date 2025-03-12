from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
def bell_each_shot() -> list[str]:
    """ Run a phi plus Bell circuit using Qiskit Sampler with the Aer simulator as backend for 10 shots and return measurement results for each shots. To do so, transpile the circuit using a pass manager with optimization level as 1.
    """
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    backend = AerSimulator()
    pass_manager = generate_preset_pass_manager("optimization_level=1")
    transpiled_qc = pass_manager.run(qc)
    sampler = Sampler(backend=backend)
    job = sampler.run(transpiled_qc, shots=10)
    result = job.result()
    return result.get_counts()

bell_each_shot()