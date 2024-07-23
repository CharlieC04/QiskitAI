from typing import Sequence
from qiskit import QuantumCircuit, transpile
from qiskit.providers.basic_provider import BasicSimulator
from qiskit.providers import Backend
from QiskitPBT.property import Property
from QiskitPBT.stats.assert_entangled import AssertEntangled
from QiskitPBT.utils import HashableQuantumCircuit
from QiskitPBT.stats.assertion import StatisticalAssertion, StandardAssertion, Assertion
from QiskitPBT.stats.measurements import Measurements
from QiskitPBT.stats.single_qubit_distributions.assert_equal import AssertEqual
from QiskitPBT.stats.single_qubit_distributions.assert_different import AssertDifferent
from QiskitPBT.stats.assert_most_frequent import AssertMostFrequent
from QiskitPBT.stats.utils.corrections import holm_bonferroni_correction
from QiskitPBT.stats.execution_optimizer import ExecutionOptimizer


class StatisticalAnalysisCoordinator:
    def __init__(self, number_of_measurements=2000, family_wise_p_value=0.05) -> None:
        self.assertions_for_property: dict[Property, list[Assertion]] = {}
        self.results: dict[Property, bool] = {}
        self.number_of_measurements = number_of_measurements
        self.family_wise_p_value = family_wise_p_value
        self.circuits_executed = 0 # for statistics

    #Assertions
    def assert_equal(self, property: Property, qubits1: int | Sequence[int], circuit1: QuantumCircuit, qubits2: int | Sequence[int], circuit2: QuantumCircuit, basis = ["x", "y", "z"]):
        # parse qubits so that assert equals always gets sequences of qubits
        if not isinstance(qubits1, Sequence):
            qubits1 = (qubits1, )
        if not isinstance(qubits2, Sequence):
            qubits2 = (qubits2, )
        # hack to make circuits in assert equals be usable as dictionary keys (by ref)
        circ1 = circuit1.copy()
        circ1.__class__ = HashableQuantumCircuit
        circ2 = circuit2.copy()
        circ2.__class__ = HashableQuantumCircuit
        if property in self.assertions_for_property:
            self.assertions_for_property[property].append(AssertEqual(qubits1, circ1, qubits2, circ2, basis))
        else:
            self.assertions_for_property[property] = [AssertEqual(qubits1, circ1, qubits2, circ2, basis)]

    def assert_different(self, property: Property, qubits1: int | Sequence[int], circuit1: QuantumCircuit, qubits2: int | Sequence[int], circuit2: QuantumCircuit, basis = ["x", "y", "z"]):
        # parse qubits so that assert equals always gets sequences of qubits
        if not isinstance(qubits1, Sequence):
            qubits1 = (qubits1, )
        if not isinstance(qubits2, Sequence):
            qubits2 = (qubits2, )
        # hack to make circuits in assert equals be usable as dictionary keys (by ref)
        circ1 = circuit1.copy()
        circ1.__class__ = HashableQuantumCircuit
        circ2 = circuit2.copy()
        circ2.__class__ = HashableQuantumCircuit

        if property in self.assertions_for_property:
            self.assertions_for_property[property].append(AssertDifferent(qubits1, circ1, qubits2, circ2, basis))
        else:
            self.assertions_for_property[property] = [AssertDifferent(qubits1, circ1, qubits2, circ2, basis)]

    def assert_entangled(self, property: Property, qubits: Sequence[int], circuit: QuantumCircuit, basis = ["z"]):
        # parse qubits so that assert equals always gets sequences of qubits
        if not isinstance(qubits, Sequence):
            qubits = (qubits,)
        # hack to make circuits in assert equals be usable as dictionary keys (by ref)
        circ = circuit.copy()
        circ.__class__ = HashableQuantumCircuit

        if property in self.assertions_for_property:
            self.assertions_for_property[property].append(AssertEntangled(qubits, circ, basis))
        else:
            self.assertions_for_property[property] = [AssertEntangled(qubits, circ, basis)]

    def assert_most_frequent(self, property: Property, qubits: int | Sequence[int], circuit: QuantumCircuit, states: str | Sequence[str], basis = ["z"]):
        # parse qubits so that assert equals always gets sequences of qubits / bitstrings
        if not isinstance(qubits, Sequence):
            qubits = (qubits,)
        if not isinstance(states, Sequence):
            marked_states = (states, )
        # hack to make circuits in assert equals be usable as dictionary keys (by ref)
        circ = circuit.copy()
        circ.__class__ = HashableQuantumCircuit

        if property in self.assertions_for_property:
            self.assertions_for_property[property].append(AssertMostFrequent(qubits, circ, states, basis))
        else:
            self.assertions_for_property[property] = [AssertMostFrequent(qubits, circ, states, basis)]
    
    # Entrypoint for analysis
    def perform_analysis(self, properties: list[Property], backend: Backend=BasicSimulator()) -> None:
        execution_optimizer = ExecutionOptimizer()
        # classical assertion failed dont run quantum
        for property in properties:
            if not property.classical_assertion_outcome:
                self.results[property] = False
                continue

            for assertion in self.assertions_for_property[property]:
                execution_optimizer.add_measurement_configuration(assertion.get_measurement_configuration())

        measurements = self._perform_measurements(execution_optimizer, backend)

        p_values = {}
        for property in properties:
            if property.classical_assertion_outcome and property not in self.results:
                p_values[property] = {}
                for assertion in self.assertions_for_property[property]:
                    if isinstance(assertion, StatisticalAssertion):
                        p_value = assertion.calculate_p_values(measurements)
                        p_values[property][assertion] = p_value
                    elif not isinstance(assertion, Assertion):
                        raise ValueError("Assertion must be a subclass of Assertion")

        # perform family wise error rate correction
        # Ideally, we need to sort all of the p-values from all assertions, then pass back the corrected alpha values to compare them to in a list

        # Only do Holm Bonferroni Correction if there are p_values to correct (preconditions pass)
        if p_values:
            expected_p_values = holm_bonferroni_correction(self.assertions_for_property, p_values, self.family_wise_p_value)

        # calculate the outcome of each assertion
        for property in properties:
            if property not in self.results:
                self.results[property] = True
            for assertion in self.assertions_for_property[property]:
                if isinstance(assertion, StandardAssertion):
                    self.results[property] = (self.results[property] and assertion.calculate_outcome(measurements))
                elif isinstance(assertion, StatisticalAssertion):
                    self.results[property] = (self.results[property] and assertion.calculate_outcome(p_values[property][assertion], expected_p_values[property][assertion]))
                else:
                    raise ValueError("The provided assertions must be a subclass of Assertion")

    # creates a dictionary of measurements for each assertion,
    def _perform_measurements(self, execution_optimizer: ExecutionOptimizer, backend: Backend) -> dict[StatisticalAssertion, Measurements]:
        measurements = Measurements()

        for circuit in execution_optimizer.get_circuits_to_execute():
            # TODO: get counts actually returns (or used to) unparsed bit strings, so if there are 2 quantum registers there is a space in there - this may need some attention
            # this is necessary for measure to work
            counts = backend.run(transpile(circuit, backend), shots=self.number_of_measurements).result().get_counts()
            self.circuits_executed += 1
            # get the original circuit, as well as basis measurements, and what assertions it is linked to
            for measurement_name, original_circuit in execution_optimizer.get_measurement_info(circuit):
                measurements.add_measurement(original_circuit, measurement_name, counts)

        return measurements
