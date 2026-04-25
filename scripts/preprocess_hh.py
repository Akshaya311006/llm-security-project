from datasets import load_dataset
import json

# -------------------------------
# LOAD DATASET
# -------------------------------
dataset = load_dataset("Anthropic/hh-rlhf", split="train")

print("Total samples:", len(dataset))


# -------------------------------
# CLEAN FUNCTION
# -------------------------------
def clean(q):
    q = str(q).lower().strip()
    return " ".join(q.split())


# -------------------------------
# EXTRACT AMBIGUOUS
# -------------------------------
AMBIGUOUS_KEYWORDS = [
    "how", "why", "what", "explain",
    "hypothetical", "for research",
    "internal", "rules", "behavior",
    "system", "instructions", "policy"
]

ambiguous = []

for item in dataset:
    text = item["chosen"]

    # Extract only Human part
    if "Human:" in text:
        q = text.split("Human:")[-1].split("Assistant:")[0]
    else:
        continue

    if any(k in q.lower() for k in AMBIGUOUS_KEYWORDS):
        ambiguous.append(clean(q))


# -------------------------------
# REMOVE DUPLICATES
# -------------------------------
ambiguous = list(set(ambiguous))


# -------------------------------
# LIMIT SIZE
# -------------------------------
ambiguous = ambiguous[:2000]


# -------------------------------
# FORMAT
# -------------------------------
ambiguous_data = [
    {"query": q, "category": "ambiguous"}
    for q in ambiguous
]

print("Ambiguous extracted:", len(ambiguous_data))


# -------------------------------
# SAVE
# -------------------------------
with open(r"E:\llm-security-project\output\hh_ambiguous.json", "w") as f:
    json.dump(ambiguous_data, f, indent=2)

print("Saved successfully!")