import json
from datasets import load_dataset

def clean(q):
    return " ".join(str(q).lower().strip().split())

# -------------------------------
# LOAD EXISTING DATA
# -------------------------------
with open(r"E:\llm-security-project\output\final_security_dataset_refined.json") as f:
    existing = json.load(f)

# -------------------------------
# LOAD DEEPSET
# -------------------------------
ds = load_dataset("deepset/prompt-injections", split="train")

# -------------------------------
# KEYWORDS (tuned for ambiguous)
# -------------------------------

# keep (borderline / probing intent)
AMBIG_STRONG = [
    "internal", "rules", "system", "behavior",
    "policy", "limitations", "model", "instructions",
    "how are you trained", "how does your system work",
    "what are your rules", "how do you respond",
    "for research", "hypothetically"
]

# remove (clearly safe)
SAFE_PATTERNS = [
    "what is", "who is", "define", "history of",
    "example of", "introduction to", "advantages of"
]

# remove (clearly attack)
ATTACK_PATTERNS = [
    "ignore", "bypass", "override", "reveal",
    "system prompt", "developer mode"
]

ambiguous = []

# -------------------------------
# 1. FROM EXISTING DATA
# -------------------------------
for item in existing:
    q = clean(item["query"])

    if item["category"] == "ambiguous":
        ambiguous.append(q)

    # convert weak injection → ambiguous
    if item["category"] == "prompt_injection":
        if any(k in q for k in ["rules", "instructions", "limitations"]):
            ambiguous.append(q)

# -------------------------------
# 2. FROM DEEPSET (label=0)
# -------------------------------
for x in ds:
    if x["label"] == 0:
        q = clean(x["text"])

        if len(q) < 15:
            continue

        # keep ambiguous-like
        if any(k in q for k in AMBIG_STRONG):

            # remove clearly safe
            if any(s in q for s in SAFE_PATTERNS):
                continue

            # remove strong attacks
            if any(a in q for a in ATTACK_PATTERNS):
                continue

            ambiguous.append(q)

# -------------------------------
# REMOVE DUPLICATES
# -------------------------------
ambiguous = list(set(ambiguous))

print("After dedup:", len(ambiguous))

# -------------------------------
# LIMIT TO 3000
# -------------------------------
ambiguous = ambiguous[:3000]

# -------------------------------
# FORMAT
# -------------------------------
ambiguous_data = [
    {"query": q, "category": "ambiguous"}
    for q in ambiguous
]

# -------------------------------
# SAVE
# -------------------------------
with open(r"E:\llm-security-project\output\ambiguous_expanded.json", "w") as f:
    json.dump(ambiguous_data, f, indent=2)

print("Saved ambiguous:", len(ambiguous_data))