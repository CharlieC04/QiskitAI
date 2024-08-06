from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import torch

base_model = "bigcode/starcoder2-3b"
cache_dir = "cache/"
finetuned = "qiskit-starcoder2-3b"
output_dir = "chralie04/qiskit-starcoder2-3b"

tokenizer = AutoTokenizer.from_pretrained(base_model, trust_remote_code=True, cache_dir=cache_dir)
model = AutoModelForCausalLM.from_pretrained(
  base_model,
  quantization_config=None,
  device_map=None,
  trust_remote_code=True,
  torch_dtype=torch.bfloat16,
  cache_dir=cache_dir
).cuda()

model = PeftModel.from_pretrained(model, finetuned, cache_dir=cache_dir)
model = model.merge_and_unload()
tokenizer.save_pretrained(output_dir)
model.save_pretrained(output_dir)
