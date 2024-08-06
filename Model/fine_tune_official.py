from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments, logging, set_seed, BitsAndBytesConfig, AutoConfig
import csv
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training, PeftModel
from peft.tuners.lora import LoraLayer
import torch
from huggingface_hub import upload_folder

import os

from ConstantLengthDataset import chars_token_ratio, ConstantLengthDataset

torch.cuda.empty_cache()

os.environ["CUDA_VISIBLE_DEVICES"] = "0,1,2"
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:512"
os.environ["TOKENIZERS_PARALLELISM"] = "true"


# HYPERPARAMETERS

MODEL = "bigcode/starcoder2-3b"



DATASET = load_dataset("csv", data_files="../Data/qiskit_dataset.csv", delimiter=",", column_names=["path", "repo", "content"], split="train", streaming=True, cache_dir="mnt/ccnas2/tdp/cc2722/cache")
print(DATASET.info)
DATA_COLUMN = "content"

SEQ_LENGTH = 2048
MAX_STEPS = 1500
BATCH_SIZE = 4
GR_ACC_STEPS = 4
LR = 3e-4
LR_SCHEDULER_TYPE = "cosine"
WEIGHT_DECAY = 0.01
NUM_WARMUP_STEPS = 100
EVAL_FREQ = 100
SAVE_FREQ = 100
LOG_FREQ = 25
OUTPUT_DIR = "qiskit-starcoder2-3b"
BF16 = False
FP16 = True

FIM_RATE = 0
FIM_SPM_RATE = 0.5

LORA_R = 8
LORA_ALPHA = 32
LORA_DROPOUT = 0.1
LORA_TARGET_MODULES = "q_proj, k_proj, v_proj, o_proj"

USE_NESTED_QUANT = True
BNB_4BIT_COMPUTE_DTYPE = "bfloat16"

SEED = 0

set_seed(SEED)

# Prepare validation and training data

valid_data = DATASET.take(450)
train_data = DATASET.skip(450)
train_data = train_data.shuffle(buffer_size=200, seed=SEED)

# Convert data into chunkable data

tokeniser = AutoTokenizer.from_pretrained(MODEL, trust_remote_code=True, cache_dir="mnt/ccnas2/tdp/cc2722/cache/")
chars_per_token = chars_token_ratio(train_data, tokeniser, DATA_COLUMN)

train_dataset = ConstantLengthDataset(tokeniser, train_data, infinite=True, seq_length=SEQ_LENGTH, chars_per_tok=chars_per_token, content_field=DATA_COLUMN, fim_rate=FIM_RATE, fim_spm_rate=FIM_SPM_RATE, seed=SEED)
eval_dataset = ConstantLengthDataset(tokeniser, valid_data, infinite=False, seq_length=SEQ_LENGTH, chars_per_tok=chars_per_token, content_field=DATA_COLUMN, fim_rate=FIM_RATE, fim_spm_rate=FIM_SPM_RATE, seed=SEED)

load_in_8bit = False

compute_dtype = getattr(torch, BNB_4BIT_COMPUTE_DTYPE)

bnb_config = BitsAndBytesConfig(
    load_in_8bit=True,
)

model = AutoModelForCausalLM.from_pretrained(
    MODEL,
    load_in_8bit=load_in_8bit,
    quantization_config=bnb_config,
    device_map="auto", # use auto for multiple GPUs
    use_cache=False,
    trust_remote_code=True,
    cache_dir="mnt/ccnas2/tdp/cc2722/cache"
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

trainer = Trainer(model=model, args=training_args, train_dataset=train_dataset, eval_dataset=eval_dataset)

trainer.train()
trainer.model.push_to_hub("chralie04/qiskit-starcoder2-3b")

