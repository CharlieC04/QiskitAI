from uuid import uuid4
from qiskit import QuantumCircuit
from QiskitPBT.stats.measurement_configuration import MeasurementConfiguration
from QiskitPBT.utils import HashableQuantumCircuit


class ExecutionOptimizer:
    def __init__(self) -> None:
        self.measurement_info_for_unique_circuits: dict[HashableQuantumCircuit, list[tuple[str, HashableQuantumCircuit]]] = {}
        self.unoptimized_measurement_info: dict[HashableQuantumCircuit, list[tuple[str, dict[int, QuantumCircuit]]]] = {}
    
    def add_measurement_configuration(self, measurement_config: MeasurementConfiguration) -> None:
        base_circuits = measurement_config.get_measured_circuits()
        for circuit in base_circuits:
            if circuit in self.unoptimized_measurement_info:
                self._ensure_unique_measurement_specifications_insertion(circuit, measurement_config.get_measurements_for_circuit(circuit))
            else:
                self.unoptimized_measurement_info[circuit] = measurement_config.get_measurements_for_circuit(circuit)
    
    # we probably dont need this as this would get optimized later on with circuits, but its probably cheaper like this then with circuit comparisons
    def _ensure_unique_measurement_specifications_insertion(self, circuit: HashableQuantumCircuit, measurement_specifications: list[tuple[str, dict[int, QuantumCircuit]]]):
        for measurement_id, qubits_measurements in measurement_specifications:
            unique = True
            # we assume the circuit is in the dict as its only called in context of self.add_measurement_configuration
            for stored_measurement_id, stored_qubits_measurements in self.unoptimized_measurement_info[circuit]:
                if measurement_id == stored_measurement_id and qubits_measurements == stored_qubits_measurements:
                    unique = False
                    break

            if unique:
                self.unoptimized_measurement_info[circuit].append((measurement_id, stored_qubits_measurements))
    
    def _optimize(self) -> list[HashableQuantumCircuit]:
        """TODO (write this properly):
            2. this optimize has to do squashing / optimizing twice:
                1. get unique base circuits (and a list of all identical circuit objects for each unique circuit)
                2. generate some best effort measurement circuits from measurement config (non overlapping qubit sets go together)
                3. once again optimize the resulting circuits (and keep a list of all identical circuit objects)
                4. probably flatten/generate a list of really unique circuits to original base circuits and their measurement info
        """
        # get unique base circuits:
        base_circuits = self.unoptimized_measurement_info.keys()
        unique_base_circuits = []
        # since we hash by reference, keep track of all duplicated circuits to feed back in get_measurement_info
        unique_circuits_to_all: dict[HashableQuantumCircuit, list[HashableQuantumCircuit]] = {}
        for circuit in base_circuits:
            try:
                inserted_circuit_idx = unique_base_circuits.index(circuit)
                unique_circuits_to_all[unique_base_circuits[inserted_circuit_idx]].append(circuit)
            except ValueError:
                unique_base_circuits.append(circuit)
                unique_circuits_to_all[circuit] = [circuit]
        
        # generate full circuits, we greedily add measurements to a circuit until we cannot add any more
        full_circuits: dict[HashableQuantumCircuit, list[tuple[str, HashableQuantumCircuit]]] = {}
        for unique_circuit in unique_base_circuits:
            full_circuits.update(self._get_full_circuits(unique_circuit, unique_circuits_to_all[unique_circuit]))

        # remove duplicates
        full_unique_circuits = []
        for full_circuit in full_circuits.keys():
            try:
                circ_idx = full_unique_circuits.index(full_circuit)
                self.measurement_info_for_unique_circuits[full_unique_circuits[circ_idx]].extend(full_circuits[full_circuit])
            except ValueError:
                full_unique_circuits.append(full_circuit)
                self.measurement_info_for_unique_circuits[full_circuit] = full_circuits[full_circuit]
    
        return full_unique_circuits

    def _get_full_circuits(self, unique_circuit: HashableQuantumCircuit, duplicate_circuits: HashableQuantumCircuit) -> dict[HashableQuantumCircuit, list[tuple[str, HashableQuantumCircuit]]]:
        all_measurement_specifications = []
        for circuit in duplicate_circuits:
            for measurement_id, qubit_spec in self.unoptimized_measurement_info[circuit]:
                all_measurement_specifications.append((measurement_id, qubit_spec, circuit))
        measurement_specification_inserted = [False for _ in all_measurement_specifications]

        full_circuits: dict[HashableQuantumCircuit, list[tuple[str, HashableQuantumCircuit]]] = {}
        while True:
            qc = unique_circuit.copy()
            qc.reset_hash()
            inserted_qubits = {}
            measurement_specifications_in_circuit = []
            if False not in measurement_specification_inserted:
                return full_circuits
            
            for i in range(len(all_measurement_specifications)):
                if measurement_specification_inserted[i]:
                    continue

                measurement_id, qubit_measurement_map, original_circuit = all_measurement_specifications[i]
                
                overlapping_qubits = set(inserted_qubits.keys()).intersection(qubit_measurement_map.keys())
                should_append_circuit = True
                
                for qubit in overlapping_qubits:
                    if inserted_qubits[qubit] != qubit_measurement_map[qubit]:
                        should_append_circuit = False
                        break
                
                if not should_append_circuit:
                    continue
                else:
                    measurement_specifications_in_circuit.append((measurement_id, original_circuit))
                    measurement_specification_inserted[i] = True
                    for qubit, measurement in qubit_measurement_map.items():
                        if qubit not in inserted_qubits:
                            qc.compose(measurement, (qubit,), (qubit,), inplace=True)
                    inserted_qubits.update(qubit_measurement_map)

            full_circuits[qc] = measurement_specifications_in_circuit

    def get_circuits_to_execute(self) -> list[QuantumCircuit]:
        """
        Returns:
            list[QuantumCircuit]: list of unique circuits to be executed based on all measurement configs added to optimizer so far
        """
        return [self._get_executable_circuit(circuit) for circuit in self._optimize()]
    
    def get_measurement_info(self, circuit: QuantumCircuit) -> list[tuple[str, HashableQuantumCircuit]]:
        """
        Args:
            circuit (QuantumCircuit): one of circuits returned by get_circuits_to_execute

        Returns:
            list[tuple[str, HashableQuantumCircuit]]: list of tuples (measurement_id, original circuit) 
                - data from measurement configuration provided to the optimizer
        """
        return self.measurement_info_for_unique_circuits[self._get_hashable_circuit(circuit)]
    
    def _get_hashable_circuit(self, circuit: QuantumCircuit) -> HashableQuantumCircuit:
        circ = circuit.copy()
        circ.__class__ = HashableQuantumCircuit
        return circ
    
    def _get_executable_circuit(self, circuit: HashableQuantumCircuit) -> QuantumCircuit:
        circ = circuit.copy()
        circ.__class__ = QuantumCircuit
        return circ
