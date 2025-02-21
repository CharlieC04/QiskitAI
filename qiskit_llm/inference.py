from transformers import AutoModelForCausalLM, AutoTokenizer
import os
import csv
import torch

class QiskitModel():
    def __init__(self, **kwargs):
        self.cache_dir = kwargs.get("cache_dir", "cache/")
        os.environ["CUDA_VISIBLE_DEVICES"] = kwargs.get("device", "0")

        model = "chralie04/qiskit-3b"

        self.tokenizer = AutoTokenizer.from_pretrained(model, cache_dir=self.cache_dir)
        self.model = AutoModelForCausalLM.from_pretrained(model, cache_dir=self.cache_dir, device_map="auto")
    
        if self.tokenizer.pad_token_id is None:
            self.tokenizer.pad_token_id = self.tokenizer.eos_token_id

    def prompt(self, **kwargs):
        if not kwargs["prompt"]:
            raise ValueError("Please ensure you pass a prompt (str) into the function")

        prompt = kwargs["prompt"]
        output_file = kwargs.get("output_file", "result.py")

        inputs = self.tokenizer.encode_plus(prompt, return_tensors="pt")
        input_ids = inputs["input_ids"].to("cuda")
        attention_mask = inputs["attention_mask"].to("cuda")
        if torch.cuda.is_available():
            input_ids = input_ids
            attention_mask = attention_mask
        
        num_outputs = kwargs.get("num_outputs", 1)
        temperature = kwargs.get("temp", 0.7)

        if num_outputs == 1:
            output = self.model.generate(input_ids, attention_mask=attention_mask, max_new_tokens=256, eos_token_id=self.tokenizer.eos_token_id)
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(self.tokenizer.decode(output[0], skip_special_tokens=True))
        else:
            outputs = self.model.generate(input_ids, attention_mask=attention_mask, max_new_tokens=256, eos_token_id=self.tokenizer.eos_token_id,
                num_return_sequences=num_outputs, do_sample=True, top_k=50, top_p=0.95, temperature=temperature)

            outputs = [self.tokenizer.decode(output, skip_special_tokens=True) for output in outputs]
            for i, output in enumerate(outputs):
                split_file = output_file.split(".")
                with open(f"{split_file[0]}{i}.{split_file[1]}", "w", encoding="utf-8") as f:
                    f.write(output)




