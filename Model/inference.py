from transformers import AutoModelForCausalLM, AutoTokenizer

model = "chralie04/qiskit-starcoder2-3b"
cache_dir = "cache/"

tokenizer = AutoTokenizer.from_pretrained(model, cache_dir=cache_dir)
model = AutoModelForCausalLM.from_pretrained(model,
  cache_dir=cache_dir
).to("cuda")

if tokenizer.pad_token_id is None:
  tokenizer.pad_token_id = tokenizer.eos_token_id

prompt = """
from qiskit.circuit.library import LinearFunction
from qiskit.synthesis.linear.linear_matrix_utils import random_invertible_binary_matrix

def get_random_linear_function(n_qubits, seed):
  # Generate a random linear function using the input parameters and the
  # random_invertible_binary_matrix method
"""

inputs = tokenizer.encode_plus(prompt, return_tensors="pt")
input_ids = inputs["input_ids"].to("cuda")
attention_mask = inputs["attention_mask"].to("cuda")

outputs = model.generate(input_ids, attention_mask=attention_mask,
  max_new_tokens=64, eos_token_id=tokenizer.eos_token_id)

with open("result.py", "w", encoding="utf-8") as f:
  f.write(tokenizer.decode(outputs[0], skip_special_tokens=True))

