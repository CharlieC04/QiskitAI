# Qiskit LLM

This repository contains a library for LLM code generation for the qiskit python library, including a RAG prompt augmentation system.

## Description


### Getting Started

The fastest way to install all required dependencies for the repository is by using the following command:
```bash
pip install -r requirements.txt
```
Note: this assumes you are using CUDA 12 for GPU inference. If you are using a different CUDA version, you should download a different version of the Pytorch library [here](https://pytorch.org/get-started/locally/).

You can also install the required libraries manually if you require different versions. The following libraries are required:
- Transformers
- Pytorch (install depending on CUDA/CPU)
- Pandas
- Datasets
- Langchain
- Langchain Community
- Sentence Transformers
- Ragatouille

Note: for training across mulitple GPUs you also need to install the Accelerate library

### Basic Usage

The following code is a basic example of how to use the model, including augmenting the prompt with RAG:

```python
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

augmented_prompt = rag.augment(
        prompt=prompt,                        # Prompt to augment
        num_docs=30,                          # Number of documents for similarity search
        num_docs_final=5                      # Final number of documents after reranking
)

model.prompt(
        prompt=prompt,                        # Prompt to respond to
        output_file="result.py",              # File to store result in
        num_outputs=1,                        # Number of different responses
        temp=0.7                       # Temperature of responses
)
```

It is possible to use the RAG system on your own custom dataset, but we provide [Qiskit Docs](https://huggingface.co/datasets/chralie04/qiskit_docs), which is a dataset created using the documentation files available on the qiskit Github repository, which includes official code examples.

Note: When outputting multiple resuts from the ```model.prompt``` fuction, each result will be saved in a separate file of the form ```result{i}.py```.

## Development

### Dataset Creation

The dataset was created by scraping Github repositories whilst searching for the keyword "Qiskit". Files in repositories were filtered by checking if they contained keywords relating to qiskit. The list of files, and repositories that they are from, can be found in the ```Training/data``` folder. 

The script for creating the dataset file, which can be found [here](https://huggingface.co/datasets/chralie04/qiskit_code_examples), is in the same folder. The files in the dataset were then chunked using the ```ConstantLengthDataset``` script, so that they could be passed into the base code generation model.

### Fine-Tuning

The script for fine tuning can be found at ```Training/tune/fine_tune.py```. The base code generation model used was the Starcoder2 3B model, which can be found [here](https://huggingface.co/bigcode/starcider2-3b). The model was trained across 4 NVIDIA GeForce RTX 3090s using LoRA optimisation. The training parameters used can be found in the tuning script.
