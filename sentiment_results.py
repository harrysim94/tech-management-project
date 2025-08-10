import json
import matplotlib.pyplot as plt

with open("sentiment_results.json", "r", encoding="utf-8") as f:
    data = json.load(f)

sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
for entry in data:
    sentiment = entry.get("sentiment")
    if sentiment in sentiment_counts:
        sentiment_counts[sentiment] += 1

labels = list(sentiment_counts.keys())
counts = [sentiment_counts[label] for label in labels]

plt.bar(labels, counts, color=["green", "red", "gray"])
plt.xlabel("Sentiment")
plt.ylabel("Count")
plt.title("Sentiment Distribution")
plt.show()
