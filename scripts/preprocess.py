import pandas as pd
from datasets import load_dataset
import json

# -------------------------------
# 1. Load HackAPrompt
# -------------------------------
df = pd.read_parquet(r"E:\llm-security-project\data\hackaprompt.parquet")

hack_queries = df["user_input"].dropna().tolist()

# Strong filtering
keywords = [
    "ignore previous", "ignore instructions", "override",
    "reveal", "system prompt", "hidden instructions",
    "bypass", "forget previous", "act as", "pretend",
    "show internal", "developer mode"
]

hack_queries = [
    q for q in hack_queries
    if any(word in q.lower() for word in keywords)
]

print("HackAPrompt:", len(hack_queries))


# -------------------------------
# 2. Load deepset dataset
# -------------------------------
dataset = load_dataset("deepset/prompt-injections")
df_deep = pd.DataFrame(dataset["train"])

deep_queries = df_deep["text"].dropna().tolist()

print("Deepset:", len(deep_queries))


# -------------------------------
# 3. Load Jasper dataset
# -------------------------------
df_jasper = pd.read_parquet(r"E:\llm-security-project\data\jasper.parquet")

print("Jasper columns:", df_jasper.columns)

# Auto column detection
if "text" in df_jasper.columns:
    jasper_queries = df_jasper["text"].dropna().tolist()
elif "prompt" in df_jasper.columns:
    jasper_queries = df_jasper["prompt"].dropna().tolist()
elif "instruction" in df_jasper.columns:
    jasper_queries = df_jasper["instruction"].dropna().tolist()
else:
    raise Exception("No valid text column found in Jasper dataset")

print("Jasper:", len(jasper_queries))


# -------------------------------
# 4. Combine ALL
# -------------------------------
all_queries = hack_queries + deep_queries + jasper_queries

print("Before cleaning:", len(all_queries))


# -------------------------------
# 5. CLEAN TEXT
# -------------------------------
def clean_text(text):
    text = text.lower().strip()
    return " ".join(text.split())

all_queries = [clean_text(q) for q in all_queries if q]


# -------------------------------
# 6. REMOVE DUPLICATES
# -------------------------------
all_queries = list(set(all_queries))

print("After dedup:", len(all_queries))


# -------------------------------
# 7. STRONG FILTERING
# -------------------------------

# Keep meaningful length
all_queries = [q for q in all_queries if 5 <= len(q.split()) <= 40]

# Keep strong injection intent
strong_keywords = [
    "ignore", "override", "bypass", "reveal",
    "system prompt", "hidden", "instructions",
    "pretend", "act as", "developer mode"
]

all_queries = [
    q for q in all_queries
    if any(word in q for word in strong_keywords)
]

print("After strong filter:", len(all_queries))


# -------------------------------
# 8. LIMIT SIZE (IMPORTANT)
# -------------------------------
TARGET_SIZE = 3500

if len(all_queries) > TARGET_SIZE:
    all_queries = all_queries[:TARGET_SIZE]

print("Final trimmed size:", len(all_queries))


# -------------------------------
# 9. FINAL FORMAT
# -------------------------------
risk_data = [
    {
        "query": q,
        "label": "HIGH_RISK",
        "category": "prompt_injection"
    }
    for q in all_queries
]

print("Final dataset size:", len(risk_data))


# -------------------------------
# 10. SAVE DATASET
# -------------------------------
with open(r"E:\llm-security-project\output\risk_data.json", "w") as f:
    json.dump(risk_data, f, indent=2)

print("Dataset saved successfully!")
