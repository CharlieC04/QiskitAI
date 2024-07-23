# class that inherits from property based test
from qiskit import QuantumCircuit
from QiskitPBT.property import Property
from QiskitPBT.input_generators.random_unitary import RandomUnitary
from QiskitPBT.case_studies.quantum_fourier_transform.quantum_fourier_transform import qft_general


class IdentityProperty(Property):
    # specify the inputs that are to be generated
    def get_input_generators(self):
        unitary = RandomUnitary(1, 10)
        return [unitary]

    # specify the preconditions for the test
    def preconditions(self, unitary):
        return True

    # specify the operations to be performed on the input
    def operations(self, unitary):
        n = unitary.num_qubits
        # perform Uxn ( Hxn ( QFT (0xn)) )

        # QFT (0xn)
        qft = qft_general(n)

        # Hxn
        for i in range(n):
            qft.h(i)

        # Uxn
        qft.append(unitary, range(n))

        # perform Uxn (0xn)
        qc = QuantumCircuit(n, n)
        qc.append(unitary, range(n))
        self.statistical_analysis.assert_equal(self, list(range(n)), qft, list(range(n)), qc)
