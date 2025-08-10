import requests
import json
import os

api_key = "686a48721f27c2a3fe182455"
url = "https://api.scrapingdog.com/google_scholar"

total_pages = 50  # Adjust as needed
start_page = 0  # Starting page number
results_per_page = 10
all_results = []

for page in range(start_page, total_pages, +1):
    params = {
        "api_key": api_key,
        "query": "disruptive technology",
        "language": "en",
        "page": page,
        "results": results_per_page,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        # Append scholar_results if present
        if "scholar_results" in data:
            all_results.extend(data["scholar_results"])
    else:
        print(
            f"Request failed for page {page} with status code: {response.status_code}"
        )

json_path = "scholar_data.json"

# Load existing data if file exists
if os.path.exists(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        existing_data = json.load(f)
else:
    existing_data = {"scholar_results": []}

# Append new results
existing_data["scholar_results"].extend(all_results)

# Save back to file
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(existing_data, f, ensure_ascii=False, indent=2)
print(f"Data from {total_pages} pages saved to scholar_data.json")
