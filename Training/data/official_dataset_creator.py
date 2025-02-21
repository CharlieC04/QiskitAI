import csv

with open("../Data/official_dataset.csv", "w", encoding="utf-8") as w:
        csv_writer = csv.writer(w, delimiter=",")
        with open("filedata.csv", "r", newline="", encoding="utf-8") as f:
                csv_reader = csv.reader(f, delimiter="|")
                row_count = 0
                for row in csv_reader:
                        if row_count == 10:
                                break
                        filepath = row[0]
                        if filepath.split("/")[0] == "official_python_code":
                                row_count += 1
                                with open(filepath, "r", encoding="utf-8") as p:
                                        python_data = p.read()
                                        csv_writer.writerow([row[1], row[2], python_data])
