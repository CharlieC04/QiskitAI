from abc import ABC, abstractmethod

from qiskit import QuantumCircuit


class InitialStrategy(ABC):
    @abstractmethod
    def set_up_initial_state_circuit(self, quantum_circuit: QuantumCircuit):
        pass


class PhaseStrategy(ABC):
    @abstractmethod
    def set_up_phase_circuit(self, gamma, quantum_circuit: QuantumCircuit):
        pass


class MixerStrategy(ABC):
    @abstractmethod
    def set_up_mixer_circuit(self, beta, quantum_circuit: QuantumCircuit):
        pass


class MeasurementStrategy(ABC):
    @abstractmethod
    def set_up_measurement_circuit(self, quantum_circuit: QuantumCircuit):
        pass
