from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
def run_bell_state_simulator():
    """ Define a phi plus bell state using Qiskit, transpile the circuit using pass manager with optimization level as 1, run it using Qiskit Sampler with the Aer simulator as backend and return the counts dictionary.
    """
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    backend = AerSimulator()
    pass_manager = generate_preset_pass_manager("optimization_level_1")
    transpiled_qc = pass_manager.run(qc)
    sampler = Sampler()
    counts = sampler.run(transpiled_qc, backend).result().get_counts()
    return counts

counts = run_bell_state_simulator()
print(counts)