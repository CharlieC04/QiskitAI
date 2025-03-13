from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments, logging, set_seed, BitsAndBytesConfig, AutoConfig, DataCollatorForSeq2Seq
import csv
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training, PeftModel
from peft.tuners.lora import LoraLayer
import torch
from huggingface_hub import upload_folder
import random

import os

from ConstantLengthDataset import chars_token_ratio, ConstantLengthDataset

import numpy as np

torch.cuda.empty_cache()

os.environ["CUDA_VISIBLE_DEVICES"] = "0,1,2,3"
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:1024"
os.environ["TOKENIZERS_PARALLELISM"] = "true"


# HYPERPARAMETERS

MODEL = "bigcode/starcoder2-7b"



DATASET = load_dataset("chralie04/qiskit_clean", split="train", streaming=False, cache_dir="cache/")
DATA_COLUMN = "content"

MAX_STEPS = 1500
BATCH_SIZE = 8
GR_ACC_STEPS = 2
LR = 3e-4
LR_SCHEDULER_TYPE = "cosine"
WEIGHT_DECAY = 0.01
NUM_WARMUP_STEPS = 100
EVAL_FREQ = 100
SAVE_FREQ = 100
LOG_FREQ = 50
OUTPUT_DIR = "qiskit-starcoder2-7b"
BF16 = False
FP16 = True

LORA_R = 8
LORA_ALPHA = 32
LORA_DROPOUT = 0.1
LORA_TARGET_MODULES = "q_proj, k_proj, v_proj, o_proj, down_proj, up_proj"

USE_NESTED_QUANT = True
BNB_4BIT_COMPUTE_DTYPE = "bfloat16"

SEED = 0

set_seed(SEED)

# Prepare validation and training data
data_split = DATASET.train_test_split(test_size=0.1, seed=SEED)
train_data = data_split["train"]
valid_data = data_split["test"]

# Convert data into chunkable data

tokeniser = AutoTokenizer.from_pretrained(MODEL, trust_remote_code=True, cache_dir="cache/")
tokeniser.pad_token = tokeniser.eos_token

def tokenise(ex):
    encoded = tokeniser(ex[DATA_COLUMN].strip(), truncation=True, max_length=2048, padding=False)
    return encoded

train_dataset = train_data.map(tokenise, remove_columns=[DATA_COLUMN])
eval_dataset = valid_data.map(tokenise, remove_columns=[DATA_COLUMN])

class DataCollator(DataCollatorForSeq2Seq):
    def __call__(self, feats):
        for feat in feats:
            feat["input_ids"].append(tokeniser.eos_token_id)
            feat["labels"] = feat["input_ids"].copy()
            if "attention_mask" in feat:
                feat["attention_mask"].append(1)
        return super().__call__(feats)

bnb_config = BitsAndBytesConfig(
    load_in_8bit=True,
)

model = AutoModelForCausalLM.from_pretrained(
    MODEL,
    load_in_8bit=False,
    quantization_config=bnb_config,
    device_map="auto", # use auto for multiple GPUs
    use_cache=False,
    trust_remote_code=True,
    cache_dir="cache/"
)

model = prepare_model_for_kbit_training(model)

model.gradient_checkpointing_enable()

peft_config = LoraConfig(
    lora_alpha=LORA_ALPHA,
    lora_dropout=LORA_DROPOUT,
    r=LORA_R,
    bias="none",
    task_type="CAUSAL_LM",
    target_modules=LORA_TARGET_MODULES.split(",")
)

model = get_peft_model(model, peft_config)

#model.print_trainable_parameters()

train_data.start_iteration = 0

output_dir = "chralie04/" + OUTPUT_DIR

training_args = TrainingArguments(
    output_dir=output_dir,
    dataloader_drop_last=True,
    evaluation_strategy="steps",
    save_strategy="steps",
    max_steps=MAX_STEPS,
    eval_steps=EVAL_FREQ,
    save_steps=SAVE_FREQ,
    logging_steps=LOG_FREQ,
    per_device_train_batch_size=BATCH_SIZE,
    per_device_eval_batch_size=BATCH_SIZE,
    learning_rate=LR,
    lr_scheduler_type=LR_SCHEDULER_TYPE,
    warmup_steps=NUM_WARMUP_STEPS,
    gradient_accumulation_steps=GR_ACC_STEPS,
    gradient_checkpointing=True,
    fp16=FP16,
    bf16=BF16,
    weight_decay=WEIGHT_DECAY,
    push_to_hub=True,
)


data_collator = DataCollator(tokenizer=tokeniser, padding=True)

trainer = Trainer(model=model, args=training_args, train_dataset=train_dataset, 
    eval_dataset=eval_dataset, data_collator=data_collator)

def compute_loss(model, inputs, return_outputs=False, **kwargs):
    input_ids = inputs["input_ids"]
    print("End of Sequence:", tokeniser.eos_token_id, "Pad Token:", tokeniser.pad_token_id)
    print("Input tokens:", input_ids[0])
    print("Text:", tokeniser.decode(input_ids[0]))
    import sys 
    sys.exit(0)
    outputs = model(**inputs)
    loss = outputs.loss
    return (loss, outputs) if return_outputs else loss

trainer.compute_loss = compute_loss

# trainer.train(resume_from_checkpoint="chralie04/qiskit-starcoder2-7b/checkpoint-800")
trainer.train()
# trainer.model.push_to_hub("chralie04/qiskit-starcoder2-7b")

