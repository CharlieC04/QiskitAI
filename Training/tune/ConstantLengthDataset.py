from tqdm import tqdm
import functools
import numpy as np
from torch.utils.data import IterableDataset
from torch.utils.data.dataloader import DataLoader
import random
import torch

def chars_token_ratio(dataset, tokeniser, data_column, nb_examples=200):
    total_chars, total_toks = 0, 0
    for _, ex in tqdm(zip(range(nb_examples), iter(dataset)), total=nb_examples):
        total_chars += len(ex[data_column])
        total_toks += len(tokeniser(ex[data_column]).tokens())
    return total_chars / total_toks


### THIS CODE IS FOR APPLYING FIM TRANSFORMATIONS

# Get ids of toks for pref, suff and middle
@functools.lru_cache(maxsize=None)
def get_fim_token_ids(tokeniser):
    try:
        F_PREFIX, F_MIDDLE, F_SUFFIX, F_PAD = tokeniser.special_tokens_map["additional_special_tokens"][1:5]
        suffix_id, prefix_id, middle_id, pad_id = (tokeniser.vocab[tok] for tok in [F_SUFFIX, F_PREFIX, F_MIDDLE, F_PAD])
    except KeyError:
        suffix_id, prefix_id, middle_id, pad_id = None, None, None, None
    return suffix_id, prefix_id, middle_id, pad_id

def permute(sample, np_rng, suffix_id, prefix_id, middle_id, pad_id, fim_rate=0.5, fim_spm_rate=0.5, truncate_or_pad=False):
    # Take sample and apply FIM with prob fim_rate. Two modes, PSM and SPM
    if np_rng.binomial(1, fim_rate):
        boundaries = list(np_rng.randint(low=0, high=len(sample) + 1, size=2))
        boundaries.sort()

        prefix = np.array(sample[:boundaries[0]], dtype=np.int64)
        middle = np.array(sample[boundaries[0]: boundaries[1]], dtype=np.int64)
        suffix = np.array(sample[boundaries[1]:], dtype=np.int64)

        if truncate_or_pad:
            new_length = suffix.shape[0] + prefix.shape[0] + middle.shape[0] + 3
            diff = new_length - len(sample)

            if diff > 0:
                if suffix.shape[0] <= diff:
                    return sample, np_rng
                suffix = suffix[:suffix.shape[0] - diff]
            elif diff < 0:
                suffix = np.concatenate([suffix, np.full((-1 * diff), pad_id)])

        if np_rng.binomial(1, fim_spm_rate):
            new_sample = np.concatenate([[prefix_id, suffix_id], suffix, [middle_id], prefix, middle])
        else:
            new_sample = np.concatenate([[prefix_id], prefix, [suffix_id], suffix, [middle_id], middle])
    else:
        new_sample = sample

    return list(new_sample), np_rng


### THIS CODE DEFINES A DATASET THAT RETURNS CONSTANT-LENGTH CHUNKS OF TOKENS
class ConstantLengthDataset(IterableDataset):
    def __init__(self, tokeniser, dataset, infinite=False, seq_length=1024, num_seqs=1024, chars_per_tok=3.5, content_field="content", fim_rate=0.5, fim_spm_rate=0.5, seed=0):
        self.tokeniser = tokeniser
        self.concat_id = tokeniser.eos_token_id
        self.dataset = dataset
        self.seq_length = seq_length
        self.infinite = infinite
        self.current_size = 0
        self.max_buffer_size = seq_length * chars_per_tok * num_seqs
        self.content_field = content_field
        self.fim_rate = fim_rate
        self.fim_spm_rate = fim_spm_rate
        self.seed = seed
        (self.suffix_id, self.prefix_id, self.middle_id, self.pad_id) = get_fim_token_ids(self.tokeniser)
        if not self.suffix_id and self.fim_rate > 0:
            print("FIM is not supported, disabling")
            self.fim_rate = 0

    def __iter__(self):
        iterator = iter(self.dataset)
        more_ex = True
        np_rng = np.random.RandomState(seed=self.seed)
        while more_ex:
            buffer, buffer_len = [], 0
            while True:
                if buffer_len >= self.max_buffer_size:
                    break
                try:
                    buffer.append(next(iterator)[self.content_field])
                    buffer_len += len(buffer[-1])
                except StopIteration:
                    if self.infinite:
                        iterator = iter(self.dataset)
                    else:
                        more_ex = False
                        break
            
            tokenised_inputs = self.tokeniser(buffer, truncation=False)["input_ids"]
            all_tok_ids = []

            for toks in tokenised_inputs:
                if self.fim_rate > 0:
                    toks, np_rng = permute(toks, np_rng, self.suffix_id, self.prefix_id, self.middle_id, self.pad_id, fim_rate=self.fim_rate, fim_spm_rate=self.fim_spm_rate, truncate_or_pad=False)
                all_tok_ids.extend(toks + [self.concat_id])

            examples = []
            for i in range(0, len(all_tok_ids), self.seq_length):
                input_ids = all_tok_ids[i:i + self.seq_length]
                if len(input_ids) == self.seq_length:
                    examples.append(input_ids)
            random.shuffle(examples)
            for example in examples:
                self.current_size += 1
                yield {
                    "input_ids": torch.LongTensor(example),
                    "labels": torch.LongTensor(example)
                }
