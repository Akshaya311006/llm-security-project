import json

def clean(q):
    return " ".join(str(q).lower().strip().split())

# -------------------------------
# LOAD FINAL DATASET
# -------------------------------
with open(r"E:\llm-security-project\output\final_dataset_v6.json") as f:
    data = json.load(f)

print("Total loaded:", len(data))

# -------------------------------
# SPLIT
# -------------------------------
ambiguous = []
others = []

for item in data:
    if item["category"] == "ambiguous":
        ambiguous.append(clean(item["query"]))
    else:
        others.append(item)

print("Ambiguous before:", len(ambiguous))


# -------------------------------
# STRONG FILTER CONDITIONS
# -------------------------------

STRONG_KEYWORDS = [
    "how", "why", "what", "explain",
    "system", "model", "rules", "behavior",
    "internal", "process", "decision",
    "trained", "working", "function"
]

WEAK_PATTERNS = [
    "what is", "who is", "define",
    "tell me", "give example",
    "history of", "types of"
]

strong_ambiguous = []

for q in ambiguous:
    # remove weak safe-like queries
    if any(w in q for w in WEAK_PATTERNS):
        continue

    # keep only meaningful ambiguous
    if any(k in q for k in STRONG_KEYWORDS) and len(q) > 20:
        strong_ambiguous.append(q)

print("After strong filter:", len(strong_ambiguous))


# -------------------------------
# REMOVE DUPLICATES (STRICT)
# -------------------------------
strong_ambiguous = list(set(strong_ambiguous))

print("After dedup:", len(strong_ambiguous))


# -------------------------------
# LIMIT TO 5000 BEST
# -------------------------------
strong_ambiguous = strong_ambiguous[:5000]

print("Final ambiguous:", len(strong_ambiguous))


# -------------------------------
# FORMAT BACK
# -------------------------------
ambiguous_final = [
    {"query": q, "category": "ambiguous"}
    for q in strong_ambiguous
]

# -------------------------------
# MERGE BACK
# -------------------------------
final_data = others + ambiguous_final

print("Final dataset size:", len(final_data))


# -------------------------------
# SAVE
# -------------------------------
with open(r"E:\llm-security-project\output\final_dataset_cleaned.json", "w") as f:
    json.dump(final_data, f, indent=2)

print("Saved successfully!")