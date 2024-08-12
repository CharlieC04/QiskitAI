import os
import glob
import csv

directory = "repo/docs/api/qiskit-transpiler-service/"
file_paths = glob.glob(os.path.join(directory, "*"))

file_data = open("docs_dataset.csv", "a", encoding="utf-8")
write_to_csv = csv.writer(file_data, delimiter=",")

for file_path in file_paths:
    if file_path.endswith(".mdx"):
        with open(file_path, "r", encoding="utf-8") as f:
            write_to_csv.writerow([f.read(), file_path])