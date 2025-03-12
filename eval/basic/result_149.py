from statistics import mode
from qiskit.primitives import BitArray
def most_common_result(bits: BitArray) -> str:
    """ Return the most common result as a string of `1`s and `0`s.
    """
    return mode(bits.to_string()).zfill(len(bits))

print(most_common_result(BitArray.from_int(10)))
print(most_common_result(BitArray.from_int(100)))
print(most_common_result(BitArray.from_int(1000)))
print(most_common_result(BitArray.from_int(10000)))
print(most_common_result(BitArray.from_int(100000)))
print(most_common_result(BitArray.from_int(1000000)))
print(most_common_result(BitArray.from_int(10000000)))
print(most_common_result(BitArray.from_int(100000000)))
print(most_common_result(BitArray.from_int(1000000000)))
print(most_common_result(BitArray.from_int(10000000000)))
print(