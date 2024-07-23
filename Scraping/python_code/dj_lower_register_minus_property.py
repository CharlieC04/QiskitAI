import random
from qiskit import QuantumCircuit
from QiskitPBT.case_studies.deutsch_jozsa.deutsch_jozsa import deutsch_jozsa_circ
from QiskitPBT.case_studies.deutsch_jozsa.dj_helpers import RandomOracleInputGenerator
from QiskitPBT.property import Property


class DeutschJozsaLowerRegisterMinus(Property):
    # specify the inputs that are to be generated
    def get_input_generators(self):
        return [RandomOracleInputGenerator(3, 10)]

    # specify the preconditions for the test
    def preconditions(self, oracle):
        return True

    # specify the operations to be performed on the input
    def operations(self, oracle: QuantumCircuit):
        circ = deutsch_jozsa_circ(oracle)

        # if oracle is constant this should be all 0
        baseline = QuantumCircuit(1, 1)
        baseline.x(0)
        baseline.h(0)

        self.statistical_analysis.assert_equal(self, [circ.num_qubits - 1], circ, [0], baseline)

