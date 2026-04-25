import json

with open(r"E:\llm-security-project\output\final_security_dataset.json") as f:
    data = json.load(f)

cleaned = []

SAFE_PATTERNS = [
    "what is", "who is", "define", "history of",
    "meaning of", "example of", "introduction to"
]

for item in data:
    q = item["query"]
    cat = item["category"]

    if cat == "ambiguous":
        # remove clearly safe queries
        if any(s in q for s in SAFE_PATTERNS):
            continue

    cleaned.append(item)

print("After cleaning:", len(cleaned))

# save
with open(r"E:\llm-security-project\output\cleaned_dataset.json", "w") as f:
    json.dump(cleaned, f, indent=2)