from qiskit_llm.inference import QiskitModel
from qiskit_llm.rag import RAG

model = QiskitModel(
        device="1",                           # Available CUDA devices
        cache_dir="cache/"                    # Directory to save models in
)

ragModel = RAG(
        device="1",                           # Available CUDA devices
        cache_dir="cache/",                   # Directory to save models in
        dataset="chralie04/qiskit_docs",      # Dataset used to build knowledge base
        chunk_size=2048                       # Chunk size for splitting documents
)


prompt = """
Import the QuantumCircuit class from the qiskit library. Then, create a quantum circuit with 3 qubits. 
Ensure to include the necessary import statement from the qiskit library
"""

model.add_rag_model(ragModel)

model.prompt(
        prompt=prompt,                        # Prompt to respond to
        output_file="result.py",              # File to store result in
        num_outputs=1,                        # Number of different responses
        temp=0.7,                             # Temperature of responses
        useRag=True,                          # Flag to augment prompt using RAG model          
        rag_params={"num_docs": 30,           # Parameters for Rag
                "num_docs_final": 5}
)