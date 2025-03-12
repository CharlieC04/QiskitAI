from qiskit import QuantumCircuit
from qiskit import qpy
def create_binary_serialization():
    """ Create a file containing the binary serialization of a Phi plus Bell state quantum circuit and write it as 'bell.qpy' in binary mode.
    """
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    qpy.dump(qc, 'bell.qpy', mode='binary')

create_binary_serialization()

from qiskit import QuantumCircuit
from qiskit import qpy
def create_text_serialization():
    """ Create a file containing the text serialization of a Phi plus Bell state quantum circuit and write it as 'bell.qpy' in text mode.
    """
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    qpy.dump(qc, 'bell.qpy', mode='text')

create_text_serialization()

from qiskit import QuantumCircuit
from qiskit import qpy
def create_binary_deserialization():
    """ Create a file containing the binary serialization of a Phi plus Bell state quantum circuit and read it as 'bell.qpy' in binary mode.
    """
    qc = qpy.load('