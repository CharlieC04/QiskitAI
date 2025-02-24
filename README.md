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

model.add_rag_model(ragModel)

model.prompt(
        prompt=prompt,                        # Prompt to respond to
        output_file="result.py",              # File to store result in
        num_outputs=1,                        # Number of different responses
        temp=0.7,                             # Temperature of responses
        useRag=True,                          # Flag to augment prompt using RAG          
        rag_params={"num_docs": 30,           # Parameters for Rag
                "num_docs_final": 5}
)
```

It is possible to use the RAG system on your own custom dataset, but we provide [Qiskit Docs](https://huggingface.co/datasets/chralie04/qiskit_docs), which is a dataset created using the documentation files available on the qiskit Github repository, which includes official code examples.

Note: When outputting multiple resuts from the ```model.prompt``` fuction, each result will be saved in a separate file of the form ```result{i}.py```.

### Downloading the Model

As well as using the library provided in this repository, you can also download the model directly from Hugging Face [here](https://huggingface.co/chralie04/qiskit-3b). We provide an example on how this could be used:
```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model = "chralie04/qiskit-3b"
tokenizer = AutoTokenizer.from_pretrained(model)
model = AutoModelForCausalLM.from_pretrained(model, device_map="auto")

prompt = """
Import the QuantumCircuit class from the qiskit library. Then, create a quantum circuit with 3 qubits. 
Ensure to include the necessary import statement from the qiskit library
"""

inputs = tokenizer.encode_plus(prompt, return_tensors="pt")
input_ids = inputs["input_ids"].to("cuda")
attention_mask = inputs["attention_mask"].to("cuda")

output = model.generate(
        input_ids,
        attention_mask=attention_mask, 
        max_new_tokens=256)
```

### Utilising Error Correction

The current error correction model used is the DeepQ-Decoding agent presented in the paper [Reinforcement Learning Decoders for Fault-Tolerant Quantum Computatino](https://arxiv.org/pdf/1810.07207), the source code for which can be found [here](https://github.com/R-Sweke/DeepQ-Decoding). This can predict the corrections needed for a surface code lattice given faulty syndromes. To use this, you need to know how logical qubits map to physical qubits on the device you are using, more specifically, the width and height of the lattice of physical qubits for one logical qubit (which we call `d`). All libraries required for this are specified in the Deep-Q repository. Here is an example on how to predict corrections necessary, which should be applied to the physical qubits:
```python
from qiskit_llm.qec import DecoderModel

fixed_configs = {"d": 5,                                     # Lattice width
        "use_Y": False,                              # If can perform Y flips (or only X and Z)
        "train_freq": 1,                             # Number of interaction steps between weight updates
        "batch_size": 32,                            # Batch size for gradient descent
        "print_freq": 250,                           # How often to print train stats
        "rolling_average_length": 500,               # Number of episodes to calculate moving average over
        "stopping_patience": 500,                    # Number of episodes to trigger early stopping
        "error_model": "X",                          # X flips or DP (depolarising noise)
        "c_layers": [[64,3,2],[32,2,1],[32,2,1]],    # Convolutional layers in DeepQ network
        "ff_layers": [[512,0.2]],                    # Feed-forward layers in DeepQ network
        "max_timesteps": 1000000,                    # Maximum training steps
        "volume_depth": 5,                           # Number of measurements each time new syndrome extracted
        "testing_length": 101,                       # Number of test episodes
        "buffer_size": 50000,                        # Number of experience tuples stored
        "dueling": True,                             # Use dueling architecture
        "masked_greedy": False,                      # Choose legal actions when acting greedily
        "static_decoder": True}                      # Should always be true when training in fault-tolerant setting

variable_configs = {"p_phys": 0.001,                         # Physical error probability
        "p_meas": 0.001,                         # Measurement error probability
        "success_threshold": 10000,              # Qubit lifetime rolling average at which training success
        "learning_starts": 1000,                 # Number of steps to contribute experience tuples before training
        "learning_rate": 0.00001,                # Learning rate for gradient descent
        "exploration_fraction": 100000,          # Time steps over which parameter for exploration is annealed
        "max_eps": 1.0,                          # Initial max epsilon (exploration parameter)
        "target_network_update_freq": 5000,      # Target network generates target Q-function
        "gamma": 0.99,                           # Discount rate when calculating Q-values
        "final_eps": 0.02}                       # Final value at which annealing epsilon is stopped

decoder = DecoderModel(fixed_configs=fixed_configs, var_configs=variable_configs)

## To train a new model. Weights will be saved at logging_dir/dqn_weights.h5f
## NOTE: This can take up to 12 hours depending on resources
decoder.train_model(True)

## To make predictions on an existing model
decoder.set_model(model_weights_path="logging_dir/dqn_weights.hf5")

# To make predictions on random noise
corrections = decoder.predict_correction(p_phys=variable_configs["p_phys"], p_meas=variable_configs["p_meas"])

# To make predictions on observed noise (replace with observed faulty syndromes)
faulty_syndromes = [np.zeros((fixed_configs["d"]+1, fixed_configs["d"]+1), int) * self.fixed_configs["d"]]

corrections = decoder.predict_correction(faulty_syndromes=faulty_syndromes, 
    p_phys=variable_configs["p_phys"], p_meas=variable_configs["p_meas"]) 
```

If you have real faulty syndrome measurements, you can replace the relevant part in the code with this data. It is important to note that training a Deep-Q agent requires a large amount of computational resources and can take more than 12 hours. This is the main limitation of using this approach in the LLM pipeline. The [Deep-Q repo](https://github.com/R-Sweke/DeepQ-Decoding) contains a trained model for physical lattice width of 5.

## Development

### Dataset Creation

The dataset was created by scraping Github repositories whilst searching for the keyword "Qiskit". Files in repositories were filtered by checking if they contained keywords relating to qiskit. The list of files, and repositories that they are from, can be found in the ```Training/data``` folder. 

The script for creating the dataset file, which can be found [here](https://huggingface.co/datasets/chralie04/qiskit_code_examples), is in the same folder. The files in the dataset were then chunked using the ```ConstantLengthDataset``` script, so that they could be passed into the base code generation model.

### Fine-Tuning

The script for fine tuning can be found at ```Training/tune/fine_tune.py```. The base code generation model used was the Starcoder2 3B model, which can be found [here](https://huggingface.co/bigcode/starcider2-3b). The model was trained across 4 NVIDIA GeForce RTX 3090s using LoRA optimisation. The training parameters used can be found in the tuning script.
