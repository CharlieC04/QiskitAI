# Copyright © 2023 HQS Quantum Simulations GmbH.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
# in compliance with the License. You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied. See the License for the specific language governing permissions and limitations under
# the License.
"""Test file for interface.py."""

import sys
from typing import Union

import pytest
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
from qoqo import Circuit
from qoqo import operations as ops
from qoqo_qiskit.interface import to_qiskit_circuit  # type:ignore


def test_basic_circuit() -> None:
    """Test basic circuit conversion."""
    circuit = Circuit()
    circuit += ops.Hadamard(0)
    circuit += ops.PauliX(1)
    circuit += ops.Identity(1)

    qc = QuantumCircuit(2)
    qc.h(0)
    qc.x(1)
    qc.id(1)

    out_circ, sim_dict = to_qiskit_circuit(circuit)

    assert out_circ == qc
    assert len(sim_dict["MeasurementInfo"]) == 0


def test_qreg_creg_names() -> None:
    """Test qreg and creg qiskit names."""
    circuit = Circuit()
    circuit += ops.DefinitionBit("cr", 2, is_output=True)
    circuit += ops.DefinitionBit("crr", 3, is_output=True)

    qr = QuantumRegister(1, "qrg")
    cr = ClassicalRegister(2, "cr")
    cr2 = ClassicalRegister(3, "crr")
    qc = QuantumCircuit(qr, cr, cr2)

    out_circ, _ = to_qiskit_circuit(circuit, qubit_register_name="qrg")

    assert out_circ == qc


def test_setstatevector() -> None:
    """Test PragmaSetStateVector operation."""
    circuit = Circuit()
    circuit += ops.PragmaSetStateVector([0, 1])

    qc = QuantumCircuit(1)
    qc.initialize([0, 1])

    out_circ, _ = to_qiskit_circuit(circuit)

    assert out_circ == qc

    circuit = Circuit()
    circuit += ops.PragmaSetStateVector([0, 1])
    circuit += ops.RotateX(0, 0.23)

    qc = QuantumCircuit(1)
    qc.initialize([0, 1])
    qc.rx(0.23, 0)

    out_circ, _ = to_qiskit_circuit(circuit)

    assert out_circ == qc


def test_repeated_measurement() -> None:
    """Test PragmaRepeatedMeasurement operation."""
    circuit = Circuit()
    circuit += ops.Hadamard(0)
    circuit += ops.Hadamard(1)
    circuit += ops.DefinitionBit("ri", 2, True)
    circuit += ops.PragmaRepeatedMeasurement("ri", 300)

    qr = QuantumRegister(2, "q")
    cr = ClassicalRegister(2, "ri")
    qc = QuantumCircuit(qr, cr)
    qc.h(0)
    qc.h(1)
    qc.measure(qr, cr)

    out_circ, sim_dict = to_qiskit_circuit(circuit)

    assert out_circ == qc
    assert ("ri", 300, None) in sim_dict["MeasurementInfo"]["PragmaRepeatedMeasurement"]


def test_measure_qubit() -> None:
    """Test MeasureQubit operation."""
    circuit = Circuit()
    circuit += ops.Hadamard(0)
    circuit += ops.PauliZ(1)
    circuit += ops.DefinitionBit("crg", 1, is_output=True)
    circuit += ops.MeasureQubit(0, "crg", 0)

    qr = QuantumRegister(2, "q")
    cr = ClassicalRegister(1, "crg")
    qc = QuantumCircuit(qr, cr)
    qc.h(0)
    qc.z(1)
    qc.measure(0, cr)

    out_circ, sim_dict = to_qiskit_circuit(circuit)

    assert out_circ == qc
    assert (0, "crg", 0) in sim_dict["MeasurementInfo"]["MeasureQubit"]


@pytest.mark.parametrize("repetitions", [0, 2, 4, "test"])
def test_pragma_loop(repetitions: Union[int, str]) -> None:
    """Test PragmaLoop operation."""
    inner_circuit = Circuit()
    inner_circuit += ops.PauliX(1)
    inner_circuit += ops.PauliY(2)

    circuit = Circuit()
    circuit += ops.Hadamard(0)
    circuit += ops.PragmaLoop(repetitions=repetitions, circuit=inner_circuit)
    circuit += ops.Hadamard(3)

    qc = QuantumCircuit(4)
    qc.h(0)
    if not isinstance(repetitions, str):
        for _ in range(repetitions):
            qc.x(1)
            qc.y(2)
    qc.h(3)

    try:
        out_circ, _ = to_qiskit_circuit(circuit)
        assert out_circ == qc
    except ValueError as e:
        assert e.args == ("A symbolic PragmaLoop operation is not supported.",)


def test_custom_gates_fix() -> None:
    """Test _custom_gates_fix method."""
    qoqo_circuit = Circuit()
    qoqo_circuit += ops.PragmaSleep([0, 3], 1.0)
    qoqo_circuit += ops.PauliX(2)
    qoqo_circuit += ops.PragmaSleep([4], 0.004)
    qoqo_circuit += ops.RotateXY(3, 0.1, 0.1)

    qr = QuantumRegister(5, "q")
    qiskit_circuit = QuantumCircuit(qr)
    qiskit_circuit.delay(1.0, qr[0], unit="s")
    qiskit_circuit.delay(1.0, qr[3], unit="s")
    qiskit_circuit.x(qr[2])
    qiskit_circuit.delay(0.004, qr[4], unit="s")
    qiskit_circuit.r(0.1, 0.1, qr[3])

    out_circ, _ = to_qiskit_circuit(qoqo_circuit)
    assert out_circ == qiskit_circuit


def test_simulation_info() -> None:
    """Test SimulationInfo dictionary."""
    circuit = Circuit()
    circuit += ops.Hadamard(0)
    circuit += ops.CNOT(0, 1)
    circuit += ops.DefinitionBit("ro", 2, True)
    circuit += ops.PragmaGetStateVector("ro", None)
    circuit += ops.PragmaGetDensityMatrix("ro", None)

    _, sim_dict = to_qiskit_circuit(circuit)

    assert sim_dict["SimulationInfo"]["PragmaGetStateVector"]
    assert sim_dict["SimulationInfo"]["PragmaGetDensityMatrix"]


# For pytest
if __name__ == "__main__":
    pytest.main(sys.argv)
