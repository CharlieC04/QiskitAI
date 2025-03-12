from typing import Dict
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler
from qiskit_ibm_runtime.options import SamplerOptions
def sampler_qiskit() -> Dict:
    """ Run a Bell circuit on Qiskit Sampler and run the circuit on the Aer simulator with the seed set as 42. Return the resulting counts dictionary.
    """
    # Create a Bell circuit
    bell_circuit = QuantumCircuit(2)
    bell_circuit.h(0)
    bell_circuit.cx(0, 1)

    # Run the circuit on Qiskit Sampler
    sampler = Sampler()
    sampler_options = SamplerOptions(seed=42)
    counts = sampler.run(bell_circuit, sampler_options=sampler_options).result().get_counts()

    # Run the circuit on the Aer simulator with the seed set as 42
    aer_simulator = AerSimulator()
    aer_simulator_counts = aer_simulator.run(bell_circuit, seed_simulator=42).result().get_counts()

    return {"Qiskit Sampler": counts, "Aer Simulator": aer_simulator_counts}

counts = sampler_qiskit()
print(counts)