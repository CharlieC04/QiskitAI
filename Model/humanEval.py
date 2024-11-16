import json
import os
import importlib.util
import tempfile
import ast
from tqdm import tqdm

from transformers import AutoModelForCausalLM, AutoTokenizer

def execute_test(task_id, test_code, function_file, entry_point):
  try:
    spec = importlib.util.spec_from_file_location("generated_function", function_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    exec_globals = {"candidate": getattr(module, entry_point)}
    exec(test_code, exec_globals)
    return "pass"
  except Exception as e:
    print(f"Test {task_id} failed with error: {e}")
    return "fail"

def process_tasks(input_file, output_file):
  with open(input_file, "r") as file:
    tasks = json.load(file)

  results = []
  for task in tqdm(tasks, desc="Evaluating tests"):
    task_id = task["task_id"]
    prompt = task["prompt"]
    test_code = task["test"]
    entry_point = task["entry_point"]
    diff = task["difficulty_scale"]

    function_code = inference(prompt)
    if function_code == "":
      print(f"Task {task_id} failed with a syntax error")
      results.append({
        "task_id": task_id,
        "difficulty_scale": diff,
        "result": "Fail"
      })
      continue
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
      function_file = temp_file.name
      temp_file.write(function_code.encode())

    result = execute_test(task_id, test_code, function_file, entry_point)

    os.remove(function_file)

    results.append({
      "task_id": task_id,
      "difficulty_scale": diff,
      "result": result
    })

    with open(output_file, "w") as file:
      json.dump(results, file, indent=4)

def remove_trailing_def(code):
  lines = code.splitlines()
  cleaned_lines = []
  in_function = False
  function_start_index = -1

  for i, line in enumerate(lines):
    stripped = line.strip()
    if stripped.startswith("def ") and not in_function:
      in_function = True
      function_start_index = i
    if in_function and (stripped == "" or not stripped.startswith(" ")):
      in_function = False
      function_start_index = -1

    if in_function and (i + 1 >= len(lines) or not lines[i + 1].startswith(" ")):
      cleaned_lines = cleaned_lines[:function_start_index]
      in_function = False
      continue

    cleaned_lines.append(line)

  if cleaned_lines[-1].startswith("def"):
    cleaned_lines.pop()
  else:
    try:
      ast.parse(cleaned_lines[-1])
    except SyntaxError:
      cleaned_lines.pop()
  

  return "\n".join(cleaned_lines)

def inference(prompt):
  inputs = tokenizer.encode_plus(prompt, return_tensors="pt")
  input_ids = inputs["input_ids"].to("cuda")
  attention_mask = inputs["attention_mask"].to("cuda")

  output = model.generate(input_ids, attention_mask=attention_mask, 
    max_new_tokens=200, eos_token_id=tokenizer.eos_token_id)
  code = tokenizer.decode(output[0], skip_special_tokens=True)
  code = remove_trailing_def(code)

  try:
    tree = ast.parse(code)
  except SyntaxError:
    return ""


  imports = []

  for node in tree.body:
    if isinstance(node, (ast.Import, ast.ImportFrom)):
      start_line = node.lineno - 1
      end_line = node.end_lineno
      import_code = "\n".join(code.splitlines()[start_line:end_line])
      imports.append(import_code)

  imports_code = "\n".join(imports) + "\n\n"

  function_code = ""

  for node in tree.body:
    if isinstance(node, ast.FunctionDef):
      start_line = node.lineno - 1
      end_line = node.end_lineno
      function_code = "\n".join(code.splitlines()[start_line:end_line])
      break
  
  return imports_code + function_code

if __name__ == "__main__":
  os.environ["CUDA_VISIBLE_DEVICES"] = "1,2"
  model = "chralie04/qiskit-starcoder2-3b"
  cache_dir = "cache/"

  input_file = "dataset_qiskit_test_human_eval.json"
  output_file = "eval_results.json"

  tokenizer = AutoTokenizer.from_pretrained(model, cache_dir=cache_dir)
  model = AutoModelForCausalLM.from_pretrained(model, cache_dir=cache_dir, device_map="auto")

  if tokenizer.pad_token_id is None:
    tokenizer.pad_token_id = tokenizer.eos_token_id

  process_tasks(input_file, output_file)
