from qiskit.circuit.library import EfficientSU2
from qiskit.quantum_info import SparsePauliOp
from qiskit.transpiler import CouplingMap
import numpy as np
from qiskit_ibm_runtime import QiskitRuntimeService, Estimator, EstimatorOptions
from qiskit.primitives.primitive_job import PrimitiveJob
from qiskit_ibm_runtime.fake_provider import FakeAuckland
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

def run_circuit_with_dd_trex() -> PrimitiveJob:
    """
    Run an EfficientSU2 circuit with 5 qubits, 2 repetitions, and pairwise entanglement on the FakeAuckland backend.
    The circuit should be transpiled with an optimization level of 1 and a transpiler seed of 789. Use 1*Z_-1 observable to calculate the expectation value.
    """
    # Create a fakeAuckland backend
    backend = FakeAuckland()

    # Create an EfficientSU2 circuit with 5 qubits, 2 repetitions, and pairwise entanglement
    qc = EfficientSU2(5, reps=2, entanglement="pairwise")

    # Transpile the circuit with optimization level 1 and transpiler seed 789
    transpiled_qc = transpile(qc, backend, optimization_level=1, seed_transpiler=789)

    # Create an EstimatorOptions object with the backend, shots, and seed
    options = EstimatorOptions(backend=backend, shots=1000, seed=1234)

    # Create an Estimator object with the transpiled circuit and options
    estimator = Estimator(transpiled_qc, options)

    # Create a PrimitiveJob object from the Estimator
    job = PrimitiveJob(estimator)

    # Run the PrimitiveJob
    result = job.result()

    # Get the expectation value from the result
    expectation_value = result.values[0]

    return job

def run_circuit_with_dd_trex_with_coup