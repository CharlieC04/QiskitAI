import requests, csv, time
from tqdm import tqdm
from datetime import datetime, timezone, timedelta
import pause


token = "access_token" + "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"
base_api_url = "https://api.github.com/"

queries = ["Qiskit", "Qiskit Examples", "Qiskit Algorithms"]
repos = set()

for query in tqdm(queries, desc="Queries:"):
    filename = "data/" + query + ".csv"
    with open(filename, "w", newline="", encoding="utf-8") as f:
        write_to_csv = csv.writer(f, delimiter="|")

    for page in tqdm(range(1, 35), desc=f"Pages for {query}:"):
        search_url = f"{base_api_url}search/repositories?q={query}&page={str(page)}&{token}"
        try:
            response = requests.get(search_url)
        except:
            print("Issue with Github API")
            continue
        while response.status_code != 200:
            if response.status_code == 403:
                stamp = datetime.fromtimestamp(int(response.headers["X-RateLimit-Reset"]), timezone.utc)
                stamp = stamp + timedelta(0,10)
                pause.until(stamp)
            try:
                response = requests.get(search_url)
            except:
                print("Issue with Github API")

        response = response.json()
        
        if response["items"]:
            for item in response["items"]:
                with open(filename, "a", newline="",encoding="utf-8") as f:
                    write_to_csv = csv.writer(f, delimiter="|")
                    name = item["name"]
                    if name not in repos:
                        repos.add(name)
                        description = item["description"]
                        stars = item["stargazers_count"]
                        watchers = item["watchers_count"]
                        main_language = item["language"]
                        score = item["score"]
                        url = item["html_url"]
                        owner = item["owner"]["login"]
                        if item["license"]:
                            license = item["license"]["name"]
                        else:
                            license = "NO LICENSE"
                        if license != "Other":
                            write_to_csv.writerow([name, description, owner, stars, watchers, main_language, url, score, license])
