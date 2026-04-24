import pandas as pd
import json

# -------------------------------
# 1. LOAD BOTH CSV FILES
# -------------------------------
df1 = pd.read_csv(r"E:\llm-security-project\data\hackaprompt_synthetic_1000.csv")
df2 = pd.read_csv(r"E:\llm-security-project\data\hackaprompt_synthetic_1000_v2.csv")
print("File1:", df1.shape)
print("File2:", df2.shape)


# -------------------------------
# 2. CHECK COLUMNS
# -------------------------------
print("Columns:", df1.columns)


# -------------------------------
# 3. EXTRACT TEXT COLUMN
# -------------------------------
# Try common names
if "user_input" in df1.columns:
    queries1 = df1["user_input"].dropna().tolist()
    queries2 = df2["user_input"].dropna().tolist()
elif "prompt" in df1.columns:
    queries1 = df1["prompt"].dropna().tolist()
elif "text" in df1.columns:
    queries1 = df1["text"].dropna().tolist()
else:
    raise Exception("No valid column found in file1")

# Same for file2
if "user_input" in df2.columns:
    queries2 = df2["user_input"].dropna().tolist()
elif "prompt" in df2.columns:
    queries2 = df2["prompt"].dropna().tolist()
elif "text" in df2.columns:
    queries2 = df2["text"].dropna().tolist()
else:
    raise Exception("No valid column found in file2")

all_queries = queries1 + queries2
print("Total synthetic raw:", len(all_queries))


# -------------------------------
# 4. CLEAN TEXT
# -------------------------------
def clean(q):
    q = str(q).lower().strip()
    return " ".join(q.split())

all_queries = [clean(q) for q in all_queries if q]


# -------------------------------
# 5. KEEP ONLY PROMPT INJECTION
# -------------------------------
KEYWORDS = [
    "ignore", "override", "bypass", "reveal",
    "system prompt", "hidden", "instructions",
    "act as", "pretend", "developer mode",
    "forget", "new task", "repeat after me"
]

filtered = [
    q for q in all_queries
    if any(k in q for k in KEYWORDS)
]

print("After filtering:", len(filtered))


# -------------------------------
# 6. REMOVE DUPLICATES
# -------------------------------
seen = set()
unique = []

for q in filtered:
    q_short = q[:200]   # compare first 100 chars
    if q_short not in seen:
        seen.add(q_short)
        unique.append(q)

filtered = unique[:300]
print("After dedup:", len(filtered))

# -------------------------------
# 7. LIMIT SIZE (IMPORTANT)
# -------------------------------
filtered = filtered[:1000]   # keep max 1000 synthetic


# -------------------------------
# 8. FORMAT DATA
# -------------------------------
synthetic_data = [
    {"query": q, "category": "prompt_injection"}
    for q in filtered
]

print("Sample synthetic:", filtered[:5])
# -------------------------------
# 9. SAVE
# -------------------------------
with open(r"E:\llm-security-project\output\clean_prompt_injection.json", "w", encoding="utf-8") as f:
    json.dump(synthetic_data, f, indent=2, ensure_ascii=False)

print("Synthetic data saved successfully!")