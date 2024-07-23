# -*- coding: utf-8 -*-

# Copyright 2018, IBM.
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.

# pylint: disable=invalid-name,missing-docstring,broad-except,no-member

from test._random_circuit_generator import RandomCircuitGenerator
from test.common import QiskitProjectQTestCase

import random
import unittest

import numpy
from scipy.stats import chi2_contingency

from qiskit import (QuantumCircuit, QuantumRegister,
                    ClassicalRegister, execute)
from qiskit import BasicAer
from qiskit_addon_projectq import ProjectQProvider


class TestQasmSimulatorProjectQ(QiskitProjectQTestCase):
    """
    Test projectq simulator.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Set up random circuits
        n_circuits = 5
        min_depth = 1
        max_depth = 10
        min_qubits = 1
        max_qubits = 4
        random_circuits = RandomCircuitGenerator(min_qubits=min_qubits,
                                                 max_qubits=max_qubits,
                                                 min_depth=min_depth,
                                                 max_depth=max_depth,
                                                 seed=None)
        for _ in range(n_circuits):
            basis = list(random.sample(random_circuits.op_signature.keys(),
                                       random.randint(2, 7)))
            if 'reset' in basis:
                basis.remove('reset')
            if 'u0' in basis:
                basis.remove('u0')
            random_circuits.add_circuits(1, basis=basis)
        cls.rqg = random_circuits

    def setUp(self):
        ProjectQ = ProjectQProvider()
        self.projectq_sim = ProjectQ.get_backend('projectq_qasm_simulator')
        self.aer_sim = BasicAer.get_backend('qasm_simulator')

    def test_gate_x(self):
        shots = 100
        qr = QuantumRegister(1)
        cr = ClassicalRegister(1)
        qc = QuantumCircuit(qr, cr, name='test_gate_x')
        qc.x(qr[0])
        qc.measure(qr, cr)
        result_pq = execute(qc, backend=self.projectq_sim,
                            shots=shots).result(timeout=30)
        self.assertEqual(result_pq.get_counts(qc), {'1': shots})

    def test_entangle(self):
        shots = 100
        N = 5
        qr = QuantumRegister(N)
        cr = ClassicalRegister(N)
        qc = QuantumCircuit(qr, cr, name='test_entangle')

        qc.h(qr[0])
        for i in range(1, N):
            qc.cx(qr[0], qr[i])
        qc.measure(qr, cr)
        result = execute(qc, backend=self.projectq_sim, shots=shots).result(timeout=30)
        counts = result.get_counts(qc)
        self.log.info(counts)
        for key, _ in counts.items():
            with self.subTest(key=key):
                self.assertTrue(key in ['0' * N, '1' * N])

    def test_random_circuits(self):
        for circuit in self.rqg.get_circuits():
            self.log.info(circuit.qasm())
            shots = 100
            result_pq = execute(circuit, backend=self.projectq_sim,
                                shots=shots).result(timeout=30)
            result_qk = execute(circuit, backend=self.aer_sim,
                                shots=shots).result(timeout=30)
            counts_pq = result_pq.get_counts(circuit)
            counts_qk = result_qk.get_counts(circuit)
            self.log.info('qasm_simulator_projectq: %s', str(counts_pq))
            self.log.info('qasm_simulator: %s', str(counts_qk))
            states = counts_qk.keys() | counts_pq.keys()
            # contingency table
            ctable = numpy.array([[counts_pq.get(key, 0) for key in states],
                                  [counts_qk.get(key, 0) for key in states]])
            result = chi2_contingency(ctable)
            self.log.info('chi2_contingency: %s', str(result))
            with self.subTest(circuit=circuit):
                self.assertGreater(result[1], 0.01)

    def test_all_bits_measured(self):
        shots = 2
        qr = QuantumRegister(2)
        cr = ClassicalRegister(1)
        qc = QuantumCircuit(qr, cr, name='all_bits_measured')
        qc.h(qr[0])
        qc.cx(qr[0], qr[1])
        qc.measure(qr[0], cr[0])
        qc.h(qr[0])
        execute(qc, backend=self.projectq_sim,
                shots=shots).result(timeout=30)


if __name__ == '__main__':
    unittest.main(verbosity=2)
