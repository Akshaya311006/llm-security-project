from datasets import load_dataset
import json

def clean(q):
    return " ".join(str(q).lower().strip().split())

print("Loading Alpaca dataset...")

# load dataset
ds = load_dataset("tatsu-lab/alpaca", split="train")

print("Total rows:", len(ds))

normal = []
seen = set()

# -------------------------------
# FILTER RULES
# -------------------------------

# ❌ remove anything related to system probing (goes to ambiguous)
BLOCK_KEYWORDS = [
    "system", "rules", "instructions", "internal",
    "policy", "behavior", "model", "training",
    "how are you trained", "how does your system"
]

# ❌ remove weak/simple patterns (too repetitive)
WEAK_PATTERNS = [
    "what is", "who is", "define", "tell me",
]

# -------------------------------
# EXTRACT
# -------------------------------
for i, row in enumerate(ds):

    if i % 5000 == 0:
        print("Processed:", i)

    instr = clean(row["instruction"])
    inp = clean(row["input"])

    # combine instruction + input (important)
    q = instr + " " + inp if inp else instr

    # length filter
    if len(q) < 15 or len(q) > 200:
        continue

    # remove system/security related
    if any(k in q for k in BLOCK_KEYWORDS):
        continue

    # remove very weak questions
    if any(q.startswith(w) for w in WEAK_PATTERNS):
        continue

    # deduplicate
    if q in seen:
        continue

    seen.add(q)
    normal.append(q)

    # limit (important)
    if len(normal) >= 1500:
        break

print("Final normal collected:", len(normal))

# -------------------------------
# FORMAT
# -------------------------------
data = [{"query": q, "category": "normal"} for q in normal]

# -------------------------------
# SAVE
# -------------------------------
output_path = r"E:\llm-security-project\output\alpaca_normal.json"

with open(output_path, "w") as f:
    json.dump(data, f, indent=2)

print("Saved successfully at:", output_path)