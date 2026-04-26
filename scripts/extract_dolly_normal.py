from datasets import load_dataset
import json

def clean(q):
    return " ".join(str(q).lower().strip().split())

ds = load_dataset("databricks/databricks-dolly-15k", split="train")

normal = []
seen = set()

BLOCK = ["system", "rules", "instructions", "policy", "internal"]

for row in ds:
    q = clean(row["instruction"])

    if len(q) < 15 or len(q) > 200:
        continue

    if any(b in q for b in BLOCK):
        continue

    if q in seen:
        continue

    seen.add(q)
    normal.append(q)

    if len(normal) >= 1500:
        break

data = [{"query": q, "category": "normal"} for q in normal]

with open(r"E:\llm-security-project\output\dolly_normal.json", "w") as f:
    json.dump(data, f, indent=2)

print("Dolly normal:", len(data))