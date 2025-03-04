from transformers import AutoTokenizer
from datasets import Dataset, load_dataset, DatasetDict
import pandas as pd

dataset = load_dataset("chralie04/qiskit_clean", cache_dir="cache/")

print(dataset.column_names)
tokenizer = AutoTokenizer.from_pretrained("bigcode/starcoder2-7b", trust_remote_code=True, cache_dir="cache/")

# def classify(ex):
#     repo = ex.get("repo", "")
#     return "official" if any(org in repo for org in ["Qiskit-Extensions", "qiskit-community", "Qiskit"]) else "unofficial"

# dataset = dataset.map(lambda x: {"source": classify(x)})

def count_tokens(ex):
     ex["tok_count"] = len(tokenizer.encode(ex["content"], add_special_tokens=True))
     return ex

dataset_list = [count_tokens(ex) for ex in dataset["train"]]

print("Total before: ", sum(ex["tok_count"] for ex in dataset_list))

# def upsample(ex):
#     return [ex] * (15 if ex["source"] == "official" else 5)

# dataset_up = []
# for ex in dataset_list:
#     dataset_up.extend(upsample(ex))

# dataset_up = Dataset.from_list(dataset_up)
# dataset_up = dataset_up.map(count_tokens)

# print("Total after: ", sum(dataset_up["tok_count"]))

# dataset_up.remove_columns(["tok_count"])
# dataset = DatasetDict({"train": dataset_up})

# dataset.push_to_hub("chralie04/qiskit_clean")