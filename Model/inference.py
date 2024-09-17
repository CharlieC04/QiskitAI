from transformers import AutoModelForCausalLM, AutoTokenizer
import os
import csv

os.environ["CUDA_VISIBLE_DEVICES"] = "1,2,3"

model = "chralie04/qiskit-starcoder2-3b"
cache_dir = "cache/"

tokenizer = AutoTokenizer.from_pretrained(model, cache_dir=cache_dir)
model = AutoModelForCausalLM.from_pretrained(model,
  cache_dir=cache_dir,
  device_map="auto"
)

if tokenizer.pad_token_id is None:
  tokenizer.pad_token_id = tokenizer.eos_token_id


prompt_no = 18
index = 0

prompt = """
Given the Following:

Original Prompt:
Make a circuit with 2 qubits and apply a Hadamard (H) gate to the first qubit. Then, create a pulse
scheduler with the following parameters: duration=256, amp=0.2 and sigma=50. Add the pulse schedule
to the circuit

Imports:
from qiskit import QuantumCircuit
from qiskit.pulse import Play, Schedule
from qiskit.pulse.library import Gaussian
from qiskit.pulse.channels import DriveChannel

Generated Code:
from qiskit import QuantumCircuit
from qiskit.pulse import Play, Schedule
from qiskit.pulse.library import Gaussian
from qiskit.pulse.channels import DriveChannel

qc = QuantumCircuit(2)
qc.h(0)
pulse = Gaussian(duration=256, amp=0.2, sigma=50)
schedule = Schedule(pulse, DriveChannel(0))
qc.add_schedule(schedule, [0])
print(qc)

Error Traceback:
File "result.py", line 9, in <module>
  schedule = Schedule(pulse, DriveChannel(0))
File "/mnt/ccnas2/tdp/cc2722/qiskit/lib/python3.8/site-packages/qiskit/pulse.schedule.py, line 167, in __init__
  self._mutable_insert(time, sched)
File "/mnt/ccnas2/tdp/cc2722/qiskit/lib/python3.8/site-packages/qiskit/pulse.schedule.py, line 402, in _mutable_insert
  self._add_timeslots(start_time, schedule)
File "/mnt/ccnas2/tdp/cc2722/qiskit/lib/python3.8/site-packages/qiskit/pulse.schedule.py, line 529, in _add_timeslot
  other_timeslots = _get_timeslots(schedule)
File "/mnt/ccnas2/tdp/cc2722/qiskit/lib/python3.8/site-packages/qiskit/pulse.schedule.py, line 1828, in _get_timeslots
  raise PulseError(f"Invalid schedule type {type(schedule)} is specified")
qiskit.pulse.exceptions.PulseError: "Invalid schedule type <class 'qiskit.pulse.library.symbolic_pulses.ScalableSymbolicPulse
is specified"
Please analyse the code and error traceback. Based on the original prompt, identify the issue in the code and
provide a corrected version. Ensure that the new code fulfills the requirements of the original prompt and
resolves the error mentioned.
"""

prompt = ""

with open("prompt.csv", "r", encoding="utf-8") as f:
  csv_reader = csv.reader(f, delimiter=",")
  for row in csv_reader:
    if index == prompt_no:
      prompt = row[0]
      break
    index += 1


inputs = tokenizer.encode_plus(prompt, return_tensors="pt")
input_ids = inputs["input_ids"].to("cuda")
attention_mask = inputs["attention_mask"].to("cuda")

#n_samples = 10

#outputs = model.generate(input_ids, attention_mask=attention_mask,
#  max_new_tokens=300, eos_token_id=tokenizer.eos_token_id,
#  num_return_sequences=n_samples, do_sample=True, top_k=50,
#  top_p=0.95, temperature=0.7)

#outputs = [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]
#for i, output in enumerate(outputs):
#  with open(f"outputs/result{i}.py", "w", encoding="utf-8") as f:
#    f.write(output.split("Generate the code here based on the provided prompt:")[1].split('`')[0])

output = model.generate(input_ids, attention_mask=attention_mask,
  max_new_tokens=500, eos_token_id=tokenizer.eos_token_id)

with open("result.py", "w", encoding="utf-8") as f:
  f.write(tokenizer.decode(output[0], skip_special_token=True).split("Generate the code here based on the provided prompt:")[1].split('`')[0])

#with open("result.py", "w", encoding="utf-8") as f:
#  f.write(tokenizer.decode(output[0], skip_special_tokens=True).split("resolves the error mentioned.")[1].split("`")[0])
