import json
from datasets import load_dataset

def clean(q):
    return " ".join(str(q).lower().strip().split())

ds = load_dataset("deepset/prompt-injections", split="train")

normal_queries = []

# suspicious keywords to REMOVE
SUSPICIOUS = [
    "system", "rules", "instructions", "prompt",
    "bypass", "ignore", "override", "reveal",
    "developer mode"
]

for x in ds:
    if x["label"] == 0:
        q = clean(x["text"])

        if len(q) < 10:
            continue

        # remove only suspicious ones
        if any(word in q for word in SUSPICIOUS):
            continue

        normal_queries.append(q)

# remove duplicates
normal_queries = list(set(normal_queries))

# limit
normal_queries = normal_queries[:1500]

normal_data = [
    {"query": q, "category": "normal"}
    for q in normal_queries
]

print("Normal samples:", len(normal_data))

with open(r"E:\llm-security-project\output\normal_data.json", "w") as f:
    json.dump(normal_data, f, indent=2)

print("Saved successfully!")