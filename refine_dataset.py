import json

# -------------------------------
# LOAD FINAL DATASET
# -------------------------------
with open(r"E:\llm-security-project\output\final_security_dataset.json") as f:
    data = json.load(f)

print("Before:", len(data))


# -------------------------------
# RULES
# -------------------------------

# ❌ clearly safe → remove from ambiguous
SAFE_PATTERNS = [
    "what is", "who is", "define",
    "history of", "meaning of",
    "example of", "introduction to"
]

# ⚠️ weak injection → convert to ambiguous
WEAK_ATTACK = [
    "your rules",
    "your instructions",
    "how do you respond",
    "what are your limits"
]


# -------------------------------
# CLEAN + RECLASSIFY
# -------------------------------
cleaned = []

for item in data:
    q = item["query"].lower()
    cat = item["category"]

    # remove very short noise
    if len(q) < 15:
        continue

    # ❌ remove safe from ambiguous
    if cat == "ambiguous":
        if any(s in q for s in SAFE_PATTERNS):
            continue

    # 🔁 convert weak injection → ambiguous
    if cat == "prompt_injection":
        if any(w in q for w in WEAK_ATTACK):
            cat = "ambiguous"

    cleaned.append({
        "query": q,
        "category": cat
    })


print("After cleaning:", len(cleaned))


# -------------------------------
# SAVE NEW DATASET
# -------------------------------
with open(r"E:\llm-security-project\output\final_security_dataset_refined.json", "w") as f:
    json.dump(cleaned, f, indent=2)

print("Refined dataset saved successfully!")