import json
from collections import defaultdict

with open("eval_results.json", "r") as file:
  results = json.load(file)

class_results = defaultdict(int)
class_counts = defaultdict(int)
pass_rate = 0

for res in results:
  if res["result"] == "pass":
    pass_rate += 1
    class_results[res["difficulty_scale"]] += 1
  class_counts[res["difficulty_scale"]] += 1

for dclass in class_results.keys():
  print(f"{dclass} tasks had {class_results[dclass] / class_counts[dclass] * 100}% accuracy")
print(f"The model had {pass_rate / len(results) * 100}% accuracy overall")
