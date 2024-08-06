from transformers import AutoModel

model = AutoModel.from_pretrained("bigcode/starcoder2-3b", cache_dir="cache/")

print(model)
