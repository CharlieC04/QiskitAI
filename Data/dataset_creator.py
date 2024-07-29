import csv
import json

with open("qiskit_dataset.csv", "w", encoding="utf-8") as w:
        csv_writer = csv.writer(w, delimiter=",")
        with open("../Scraping/filedata.csv", "r", newline="", encoding="utf-8") as f:
                csv_reader = csv.reader(f, delimiter="|")
                for row in csv_reader:
                        try:
                            filepath = row[0]
                            if filepath.split("/")[0] == "official_python_code" or filepath.split("/")[0] == "python_code":
                                    with open("../Scraping/" + filepath, "r", encoding="utf-8") as p:
                                            python_data = p.read()
                                            csv_writer.writerow([row[1], row[2], python_data])
                            elif filepath.split("/")[0] == "notebooks" or filepath.split("/")[0] == "official_notebooks":
                                    with open("../Scraping/" + filepath, "r", encoding="utf-8") as p:
                                            notebook = json.load(p)
                                    code_cells = []
                                    for cell in notebook["cells"]:
                                            if cell["cell_type"] == "code":
                                                    code_cells.append("".join(cell["source"]))
                                    code = "\n\n".join(code_cells)
                                    if row[2] == "HuangJunye":
                                           print("Code: ", code)
                                    if code != "":
                                        csv_writer.writerow([row[1], row[2], code])
                        except Exception:
                            pass