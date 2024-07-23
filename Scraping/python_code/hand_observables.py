# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.


import qiskit

from qiskit import execute

# Observables made by hand, those observables are changed
# for the more general function sample_hamiltonian


def _measure_zz_circuit(qc: qiskit.QuantumCircuit) -> qiskit.QuantumCircuit:
    """Construct the circuit to measure"""
    zz_circuit = qc.copy()
    zz_circuit.measure_all()

    return zz_circuit


def _clear_counts(count: dict) -> dict:

    if "00" not in count:
        count["00"] = 0
    if "01" not in count:
        count["01"] = 0
    if "10" not in count:
        count["10"] = 0
    if "11" not in count:
        count["11"] = 0

    return count


def measure_zz(qc, backend, shots=10000):
    """Measure the ZZ expectation value for a given circuit."""
    zz_circuit = _measure_zz_circuit(qc)

    count = execute(zz_circuit, backend=backend, shots=shots).result().get_counts()
    count = _clear_counts(count)

    # Get total counts in order to obtain the probability
    total_counts = count["00"] + count["11"] + count["01"] + count["10"]
    # Get counts for expected value
    zz_meas = count["00"] + count["11"] - count["01"] - count["10"]
    return zz_meas / total_counts


def measure_zi(qc, backend, shots=10000):
    """Measure the ZI expectation value for a given circuit."""
    zi_circuit = _measure_zz_circuit(qc)

    count = execute(zi_circuit, backend=backend, shots=shots).result().get_counts()
    count = _clear_counts(count)

    # Get total counts in order to obtain the probability
    total_counts = count["00"] + count["11"] + count["01"] + count["10"]
    # Get counts for expected value
    zi_meas = count["00"] - count["11"] + count["01"] - count["10"]
    return zi_meas / total_counts


def measure_iz(qc, backend, shots=10000):
    """Measure the IZ expectation value for a given circuit."""
    iz_circuit = _measure_zz_circuit(qc)

    count = execute(iz_circuit, backend=backend, shots=shots).result().get_counts()
    count = _clear_counts(count)

    # Get total counts in order to obtain the probability
    total_counts = count["00"] + count["11"] + count["01"] + count["10"]
    # Get counts for expected value
    iz_meas = count["00"] - count["11"] - count["01"] + count["10"]
    return iz_meas / total_counts


def measure_xx(qc, backend, shots=10000):
    """Measure the XX expectation value for a given circuit."""

    def _measure_xx_circuit(
        qc: qiskit.QuantumCircuit,
    ) -> qiskit.QuantumCircuit:
        """Construct the circuit to measure"""
        xx_circuit = qc.copy()
        xx_circuit.h(xx_circuit.qregs[0])
        xx_circuit.measure_all()

        return xx_circuit

    xx_circuit = _measure_xx_circuit(qc)

    count = execute(xx_circuit, backend=backend, shots=shots).result().get_counts()
    count = _clear_counts(count)

    # Get total counts in order to obtain the probability
    total_counts = count["00"] + count["11"] + count["01"] + count["10"]
    # Get counts for expected value
    xx_meas = count["00"] + count["11"] - count["01"] - count["10"]
    return xx_meas / total_counts


def measure_yy(qc, backend, shots=10000):
    """Measure the YY expectation value for a given circuit."""

    def _measure_yy_circuit(
        qc: qiskit.QuantumCircuit,
    ) -> qiskit.QuantumCircuit:
        """Construct the circuit to measure"""

        yy_meas = qc.copy()
        yy_meas.barrier(range(2))
        yy_meas.sdg(range(2))
        yy_meas.h(range(2))
        yy_meas.measure_all()
        return yy_meas

    yy_circuit = _measure_yy_circuit(qc)

    count = execute(yy_circuit, backend=backend, shots=shots).result().get_counts()
    count = _clear_counts(count)

    # Get total counts in order to obtain the probability
    total_counts = count["00"] + count["11"] + count["01"] + count["10"]
    # Get counts for expected value
    xx_meas = count["00"] + count["11"] - count["01"] - count["10"]
    return xx_meas / total_counts
