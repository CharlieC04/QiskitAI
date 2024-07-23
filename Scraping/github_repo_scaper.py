import csv, os, stat, time
from git import Repo
from tqdm import tqdm

def rmtree(top):
    time.sleep(10)
    for root, dirs, files in os.walk(top, topdown=False):
        for name in files:
            filename = os.path.join(root, name)
            os.chmod(filename, stat.S_IWRITE)
            os.remove(filename)
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(top)

file_data = open("filedata.csv", "a", newline="", encoding="utf-8")
write_to_csv = csv.writer(file_data, delimiter="|")

for file in tqdm(["Qiskit Algorithms.csv", "Qiskit Examples.csv"], desc="Files"):
    if file.endswith(".csv"):
        with open(f"data/{file}", "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter="|")
            for row in tqdm(reader, desc=f"Repos in {file}"):
                url = row[6]
                owner = row[2]
                official = owner in ["Qiskit", "qiskit-community", "Qiskit-Extensions"]
                try:
                    repo = Repo.clone_from(url, "repo/")
                    for root, _, files in os.walk("repo/"):
                        for file in files:
                            if file.endswith(".py"):
                                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                                    data = f.read()
                                    if "import qiskit" in data or "from qiskit import" in data:
                                        file_name = f"python_code/{file}" if not official else f"official_python_code/{file}"
                                        write_to_csv.writerow([file_name, url, owner, row[3]])
                                        with open(file_name, "w", encoding="utf-8") as cf:
                                            cf.write(data)
                            if file.endswith(".ipynb"):
                                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                                    data = f.read()
                                    file_name = f"notebooks/{file}" if not official else f"official_notebooks/{file}"
                                    write_to_csv.writerow([file_name, url, owner, row[3]])
                                    with open(file_name, "w", encoding="utf-8") as cf:
                                        cf.write(data)
                    rmtree("repo")
                except Exception as e:
                    print(e)
                    if os.path.isdir("repo"):
                        rmtree("repo")
