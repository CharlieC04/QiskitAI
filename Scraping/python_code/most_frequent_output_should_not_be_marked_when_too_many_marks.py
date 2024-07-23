import random

import numpy as np

from qiskit import QuantumCircuit
from QiskitPBT.case_studies.grovers_algorithm.grovers_algorithm import grovers_algorithm
from QiskitPBT.case_studies.grovers_algorithm.grovers_algorithm_helpers import RandomGroversOracleMarkedStatesPairGenerator
from QiskitPBT.property import Property


class GroversAlgorithmMostFrequentNotMarkedIfTooManyMarked(Property):
    # specify the inputs that are to be generated
    def get_input_generators(self):
        return [RandomGroversOracleMarkedStatesPairGenerator(4, 7, "too_many")]

    # specify the preconditions for the test
    def preconditions(self, oracle_pair):
        oracle, marked_states = oracle_pair
        # need more than half for this property to hold
        if len(marked_states) < 2**(oracle.num_qubits//2):
            return False
        return True

    # specify the operations to be performed on the input
    def operations(self, oracle_pair):
        oracle, marked_states = oracle_pair

        # for this case to work out, we need to apply at least 1 grover iteration (we would otherwise get 0)
        n_iterations = 1

        circ = grovers_algorithm(oracle, n_iterations)

        # invert most frequent list to get the list of states that are not marked
        not_marked_states = list(set(range(2**(circ.num_qubits-1))) - set(marked_states))

        not_marked_binary_states = []
        # marked states to binary strings to check
        for state in not_marked_states:
            binary = bin(state)[2:]
            binary = '0' * (oracle.num_qubits - 1 - len(binary)) + binary
            binary = binary[::-1]
            not_marked_binary_states.append(binary)

        # TODO: need to implement this assert most frequent, or something like it, all i know about the output state
        # is that the most frequent state should be from the list of marked, and (roughly) all should have the same distribution
        # but maybe testing that is not easy to implement with what we have
        self.statistical_analysis.assert_most_frequent(self, list(range(circ.num_qubits-1)), circ, not_marked_binary_states, basis=["z"])

