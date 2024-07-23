from qiskit import *

def get_result(qc, shots=1024):
    """Runs the circuit on the simulator"""
    backend = Aer.get_backend('qasm_simulator')

    result = execute(qc, backend, shots = shots).result()
    counts = result.get_counts()
    return counts

def parse_result(counts, p=False):
    """Returns the maximum value found and optionally prints all results"""
    max = [0, 0]

    for i in counts:
        num = int(i, 2)
        key = str(num)
        value = str(counts[i])

        if (int(counts[i]) > int(max[1])):
            max[0] = num
            max[1] = value

        if p:
            print(key + ": " +  value)

    return max