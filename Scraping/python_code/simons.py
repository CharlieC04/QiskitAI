from pprint import pprint
import numpy as np
import argparse
from collections import defaultdict

from qiskit import IBMQ, Aer
from qiskit.providers.ibmq import least_busy
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute

from qiskit.visualization import plot_histogram
from sympy import Matrix, mod_inverse

from qiskit import IBMQ
from qiskit.tools.monitor import job_monitor
from qiskit.providers.ibmq import least_busy
#IBMQ.save_account('<your acct number>')


class Simons(object):
    def __init__(self, n, f):
        self._qr = QuantumRegister(2*n)
        self._cr = ClassicalRegister(n)
        self._oracle = self._create_oracle(f)

    def _create_oracle(self, f):
        n = len(list(f.keys())[0])
        U = np.zeros(shape=(2 ** (2 * n), 2 ** (2 * n)))
        for a in range(2 ** n):
            ab = np.binary_repr(a, n)
            for k, v in f.items():
                U[int(ab + k, 2), int(xor(ab, v) + k, 2)] = 1
        return U

    def _create_circuit(self, oracle):
        circuit = QuantumCircuit(self._qr, self._cr)
        circuit.h(self._qr[:len(self._cr)])
        circuit.barrier()
        circuit.unitary(oracle, self._qr, label='oracle')
        circuit.barrier()
        circuit.h(self._qr[:len(self._cr)])
        circuit.measure(self._qr[:len(self._cr)], self._cr)
        return circuit

    def _solve(self, counts):
        # reverse inputs, remove all zero inputs, and sort
        counts = [(k[::-1], v) for k, v in counts.items()
                if not all([x == '0' for x in k])]
        counts.sort(key=lambda x: x[1], reverse=True)

        # construct sympy matrix
        matrix = Matrix([[int(i) for i in k] for k, _ in counts])

        # gaussian elimination mod 2
        matrix = matrix.rref(iszerofunc=lambda x: x % 2 == 0)
        matrix = matrix[0].applyfunc(lambda x: mod(x, 2))

        # extract string
        n_rows, _ = matrix.shape
        s = [0] * len(self._cr)
        for r in range(n_rows):
            yi = [i for i, v in enumerate(list(matrix[r, :])) if v == 1]
            if len(yi) == 2:
                s[yi[0]] = '1'
                s[yi[1]] = '1'
        return s[::-1]
    
    def run(self, shots=1024, provider=None):
        circuit = self._create_circuit(self._oracle)

        if provider is None:
            # run the program on a QVM
            simulator = Aer.get_backend('qasm_simulator')
            job = execute(circuit, simulator, shots=shots)
        else:
            backend = least_busy(provider.backends(filters=lambda x: x.configuration().n_qubits >= len(self._qr) and 
                                   not x.configuration().simulator and x.status().operational==True))
            
            print("least busy backend: ", backend)
            job = execute(circuit, backend=backend, shots=shots, optimization_level=3)

            job_monitor(job, interval=2)
        try:
            results = job.result()
        except:
            raise Exception(job.error_message())
        counts = results.get_counts()
        print('Generated circuit: ')
        print(circuit.draw())
        print('Circuit output:')
        print(counts)
        print("Time taken:", results.time_taken)
        return self._solve(counts)


def mod(x, modulus):
    numer, denom = x.as_numer_denom()
    return numer * mod_inverse(denom, modulus) % modulus


def xor(x, y):
    assert len(x) == len(y)
    n = len(x)
    return format(int(x, 2) ^ int(y, 2), f'0{n}b')


def one_to_one_mapping(s):
    n = len(s)
    form_string = "{0:0" + str(n) + "b}"
    bit_map_dct = {}
    for idx in range(2 ** n):
        bit_string = np.binary_repr(idx, n)
        bit_map_dct[bit_string] = xor(bit_string, s)
    return bit_map_dct


def two_to_one_mapping(s):
    mapping = one_to_one_mapping(s)
    n = len(mapping.keys()) // 2

    new_range = np.random.choice(list(sorted(mapping.keys())), replace=False, size=n).tolist()
    mapping_pairs = sorted([(k, v) for k, v in mapping.items()], key=lambda x: x[0])

    new_mapping = {}
    # f(x) = f(x xor s)
    for i in range(n):
        x = mapping_pairs[i]
        y = new_range[i]
        new_mapping[x[0]] = y
        new_mapping[x[1]] = y

    return new_mapping


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('string', help='Secret string s of length n')
    parser.add_argument('ftype', type=int, help='1 for one-to-one or 2 for two-to-one')
    parser.add_argument('--ibmq', action='store_true', help='Run on IBMQ')
    args = parser.parse_args()

    if args.ibmq:
        try:
            provider = IBMQ.load_account()
        except:
            raise Exception("Could not find saved IBMQ account.")

    assert all([x == '1' or x == '0' for x in args.string]), 'string argument must be a binary string.'

    n = len(args.string)
    if args.ftype == 1:
        mapping = one_to_one_mapping(args.string)
    elif args.ftype == 2:
        mapping = two_to_one_mapping(args.string)
    else:
        raise ValueError('Invalid function type.')

    print('Generated mapping:')
    pprint(mapping)
    simons = Simons(n, mapping)
    result = simons.run(provider=provider if args.ibmq else None)
    result = ''.join([str(x) for x in result])
    # Check if result satisfies two-to-one function constraint
    success = np.array([mapping[x] == mapping[xor(x, result)] for x in mapping.keys()]).all() and not all([x == '0' for x in result])
    if success:
        print(f'Oracle function is two-to-one with s = {result}.')
    else:
        print('Oracle is one-to-one.')

if __name__ == '__main__':
    main()