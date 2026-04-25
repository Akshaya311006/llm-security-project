import pandas as pd
from datasets import load_dataset
import json
def clean(q):
    q = str(q).lower().strip()
    return " ".join(q.split())
# -------------------------------
# 1. LOAD DATASET
# -------------------------------
dataset = load_dataset("deepset/prompt-injections")
df = pd.DataFrame(dataset["train"])

print("Columns:", df.columns)

# -------------------------------
# 2. SPLIT DATA
# -------------------------------
# Injection
df_injection = df[df["label"] == 1]

# Normal (contains safe + ambiguous)
df_normal = df[df["label"] == 0]


# -------------------------------
# 3. EXTRACT PROMPT INJECTION
# -------------------------------
injection_queries = [clean(q) for q in df_injection["text"].dropna().tolist()]
injection_data = [
    {"query": q.strip(), "category": "prompt_injection"}
    for q in injection_queries
]

print("Injection:", len(injection_data))


# -------------------------------
# 4. EXTRACT AMBIGUOUS (FILTER)
# -------------------------------
AMBIGUOUS_KEYWORDS = [
    "how", "why", "what", "explain",
    "hypothetical", "for research",
    "internal", "rules", "behavior",
    "system", "instructions"
]

ambiguous_queries = [
    clean(q) for q in df_normal["text"].dropna().tolist()
    if any(k in q.lower() for k in AMBIGUOUS_KEYWORDS)
]

# remove duplicates
ambiguous_queries = list(set(ambiguous_queries))

# limit size
ambiguous_queries = ambiguous_queries[:1500]

ambiguous_data = [
    {"query": q.strip(), "category": "ambiguous"}
    for q in ambiguous_queries
]

print("Ambiguous:", len(ambiguous_data))

ambiguous_queries = [q for q in ambiguous_queries if len(q) > 20]
injection_queries = [q for q in injection_queries if len(q) > 20]
# -------------------------------
# 5. MERGE BOTH
# -------------------------------
final_data = injection_data + ambiguous_data

print("Total:", len(final_data))


# -------------------------------
# 6. SAVE
# -------------------------------
with open(r"E:\llm-security-project\output\deepset_combined.json", "w") as f:
    json.dump(final_data, f, indent=2)

print("Saved successfully!")