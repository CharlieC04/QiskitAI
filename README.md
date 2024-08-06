# Qiskit LLM

## Data Collection

All code for data collection can be found under Scraping. Github repositories were scraped based on Qiskit related queries. Python files and jupyter notebooks including qiskit code were then extracted and separated into official and non-official sources.
The collected files were then formatted into csv datasets in the Data folder

## Training

The base model used is the Starcoder2 3B. This was trained on the dataset across multiple GPUs. The data was converted into constant length chunks using the code in Model/ConstantLengthDataset. The tuning parameters can be found in Model/fine_tune_offical

## Inference

Inference is done in Model/inference. The prompt variable can be changed to change what the model will output. The model will output to Model/result
