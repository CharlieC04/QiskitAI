from qiskit_llm.inference import QiskitModel
from qiskit_llm.rag import RAG

model = QiskitModel(device="1")
ragModel = RAG(device="1")

prompt = """
Import the QuantumCircuit class from the qiskit library. Then, create a quantum circuit with 3 qubits. 
Ensure to include the necessary import statement from the qiskit library
"""

augmented_prompt = rag.augment(prompt)
model.prompt(prompt=prompt)