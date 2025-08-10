import json
import re
from collections import Counter
import matplotlib.pyplot as plt


def extract_years(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)
    years = []
    for result in data.get("scholar_results", []):
        displayed_link = result.get("displayed_link", "")
        match = re.search(r"\b(19|20)\d{2}\b", displayed_link)
        if match:
            year = int(match.group())
            # Only include years between 1995 and 2025
            if 1995 <= year <= 2025:
                years.append(year)
    return years


years_innovation = extract_years("scholar_data_innovation.json")
years_technology = extract_years("scholar_data_technology.json")

year_counts_innovation = Counter(years_innovation)
year_counts_technology = Counter(years_technology)

all_years = set(year_counts_innovation.keys()) | set(year_counts_technology.keys())
if all_years:
    start_year = min(all_years)
    end_year = min(max(all_years), 2025)
    years_range = list(range(start_year, end_year + 1))
    counts_innovation = [year_counts_innovation.get(year, 0) for year in years_range]
    counts_technology = [year_counts_technology.get(year, 0) for year in years_range]

    plt.figure(figsize=(10, 6))
    plt.bar(
        years_range,
        counts_innovation,
        color="skyblue",
        alpha=0.7,
        label="'Disruptive Innovation'",
    )
    plt.bar(
        years_range,
        counts_technology,
        color="orange",
        alpha=0.5,
        label="'Disruptive Technology'",
        bottom=counts_innovation,
    )
    plt.xlabel("Publication Year", fontsize=12)
    plt.ylabel("Number of Articles", fontsize=12)
    plt.title("Number of Articles Published per Year (1995-2025)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.legend()
    plt.show()
else:
    print("No valid publication years found.")
