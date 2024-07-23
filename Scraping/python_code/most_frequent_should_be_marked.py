import random

import numpy as np

from qiskit import QuantumCircuit
from QiskitPBT.case_studies.grovers_algorithm.grovers_algorithm import grovers_algorithm
from QiskitPBT.case_studies.grovers_algorithm.grovers_algorithm_helpers import RandomGroversOracleMarkedStatesPairGenerator
from QiskitPBT.property import Property


class GroversAlgorithmMostFrequentMarked(Property):
    # specify the inputs that are to be generated
    def get_input_generators(self):
        return [RandomGroversOracleMarkedStatesPairGenerator(4, 6)]

    # specify the preconditions for the test
    def preconditions(self, oracle_pair):
        oracle, marked_states = oracle_pair
        if len(marked_states) == 0 or len(marked_states) > 2**(oracle.num_qubits - 1) - 1:
            return False
        return True

    # specify the operations to be performed on the input
    def operations(self, oracle_pair):
        oracle, marked_states = oracle_pair

        # one qubit is workspace
        N = 2**(oracle.num_qubits-1)
        # number of marked states is used to identify the number of grover iterations to apply
        M = len(marked_states)

        binary_states = []
        # marked states to binary strings to check
        for state in marked_states:
            binary = bin(state)[2:]
            binary = '0' * (oracle.num_qubits - 1 - len(binary)) + binary
            binary = binary[::-1]
            binary_states.append(binary)

        # src Nielsen and Chuang, quantum computation and quantum information
        n_iterations = int(np.floor((np.pi/4) * np.sqrt((N/M))))

        circ = grovers_algorithm(oracle, n_iterations)



        # TODO: need to implement this assert most frequent, or something like it, all i know about the output state
        # is that the most frequent state should be from the list of marked, and (roughly) all should have the same distribution
        # but maybe testing that is not easy to implement with what we have
        self.statistical_analysis.assert_most_frequent(self, list(range(circ.num_qubits-1)), circ, binary_states, basis=["z"])

