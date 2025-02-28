from transformers import AutoModelForCausalLM, AutoTokenizer
import os
import csv
import torch
from peft import PeftModel

class QiskitModel():
    def __init__(self, **kwargs):
        """
        This function can take the following arguments:
        - cache_dir: directory in which to download models
        - device: cuda device to load model on, for one GPU the default is 0
        """

        self.cache_dir = kwargs.get("cache_dir", "cache/")
        os.environ["CUDA_VISIBLE_DEVICES"] = kwargs.get("device", "0")

        base_model = "bigcode/starcoder2-3b"
        model = "chralie04/qiskit-starcoder2-3b"

        # Create tokenizer and model, loaded onto appropriate devices
        self.tokenizer = AutoTokenizer.from_pretrained("bigcode/starcoder2-3b", cache_dir=self.cache_dir)
        base_model = AutoModelForCausalLM.from_pretrained(base_model, cache_dir=self.cache_dir, device_map="auto")
        self.model = PeftModel.from_pretrained(base_model, model)
        self.model.merge_and_unload()
        #self.model = AutoModelForCausalLM.from_pretrained(model, cache_dir=self.cache_dir, device_map="auto")

        if self.tokenizer.pad_token_id is None:
            self.tokenizer.pad_token_id = self.tokenizer.eos_token_id

        self.rag_model = None

    # Function to add RAG model to inference pipeline
    def add_rag_model(model):
        self.rag_model = model

    # Function to generate responses to a prompt
    def prompt(self, **kwargs):
        """
        This function can take the following arguments:
        - prompt: prompt to complete (not optional)
        - output_file: file to save generated answer to
        - num_outputs: number of responses to generate
        - temp: temperature of responses
        """

        if not kwargs["prompt"]:
            raise ValueError("Please ensure you pass a prompt (str) into the function")

        prompt = f"""<fim_prefix>{kwargs["prompt"]}<fim_suffix><fim_middle>"""
        #prompt = kwargs["prompt"]
        output_file = kwargs.get("output_file", "result.py")

        self.model.eval()

        # Augment prompt with RAG if flag set
        if kwargs.get("useRag", False):
            if self.rag_model is None:
                raise AttributeError("Please initialise RAG model")

            rag_params = kwargs.get("rag_params", {})
            if "num_docs" in rag_params and "num_docs_final" in rag_params:
                prompt = self.rag_model.augment(prompt, 
                    rag_params["num_docs"], rag_params["num_docs_final"])
            else:
                prompt = self.rag_model.augment(prompt)

        # Get ids and attention mask from tokenizer
        inputs = self.tokenizer.encode_plus(prompt, return_tensors="pt")
        input_ids = inputs["input_ids"].to("cuda")
        attention_mask = inputs["attention_mask"].to("cuda")
        if torch.cuda.is_available():
            input_ids = input_ids
            attention_mask = attention_mask
        
        num_outputs = kwargs.get("num_outputs", 1)
        temperature = kwargs.get("temp", 0.7)

        # If only one output, generate and save in file
        if num_outputs == 1:
            output = self.model.generate(input_ids, attention_mask=attention_mask, max_new_tokens=128, temperature=0.2,
                         top_k=50, top_p=0.95, do_sample=True, repetition_penalty=1.0)
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(self.tokenizer.batch_decode(output, skip_special_tokens=True)[0])
        
        # If n>1 outputs, generate all and save in numbered files
        else:
            outputs = self.model.generate(input_ids, attention_mask=attention_mask, max_new_tokens=256, eos_token_id=self.tokenizer.eos_token_id,
                num_return_sequences=num_outputs, do_sample=True, top_k=50, top_p=0.95, temperature=temperature)

            outputs = [self.tokenizer.decode(output, skip_special_tokens=True) for output in outputs]
            for i, output in enumerate(outputs):
                split_file = output_file.split(".")
                with open(f"{split_file[0]}{i}.{split_file[1]}", "w", encoding="utf-8") as f:
                    f.write(output)




