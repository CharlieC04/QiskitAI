from typing import Sequence
from qiskit import QuantumCircuit

from QiskitPBT.utils import HashableQuantumCircuit


class MeasurementConfiguration:
    def __init__(self) -> None:
        self._data: dict[HashableQuantumCircuit, list[tuple[str, dict[int, QuantumCircuit]]]] = {}
    
    def add_measurement(self, measurement_id: str, circuit: QuantumCircuit, measurement_specification: dict[int, QuantumCircuit]) -> None:
        if circuit in self._data:
            self._data[circuit].append((measurement_id, measurement_specification))
        else:
            self._data[circuit] = [(measurement_id, measurement_specification)]

    def get_measured_circuits(self) -> tuple[HashableQuantumCircuit]:
        return tuple(self._data.keys())
    
    def get_measurements_for_circuit(self, circuit: HashableQuantumCircuit) -> list[tuple[str, dict[int, QuantumCircuit]]]:
        return self._data[circuit]