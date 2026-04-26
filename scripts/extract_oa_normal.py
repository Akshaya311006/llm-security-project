from datasets import load_dataset
import json

def clean(q):
    return " ".join(str(q).lower().strip().split())

print("Loading OpenAssistant dataset...")

ds = load_dataset("OpenAssistant/oasst1", split="train")

print("Total rows:", len(ds))

normal = []
seen = set()

# -------------------------------
# FILTER RULES
# -------------------------------

# ❌ remove system / ambiguous probing
BLOCK = [
    "system", "rules", "instructions", "internal",
    "policy", "behavior", "model", "training",
    "how does your system", "how are you trained",
    "what are your rules", "your limitations"
]

# ❌ remove unsafe / attack patterns
ATTACK = [
    "ignore previous instructions", "bypass",
    "override", "reveal", "jailbreak"
]

# ❌ remove very weak queries
WEAK = [
    "what is", "who is", "define"
]

# -------------------------------
# EXTRACT
# -------------------------------
for i, row in enumerate(ds):

    if i % 5000 == 0:
        print("Processed:", i)

    # OpenAssistant uses "prompter"
    if row["role"] != "prompter":
        continue

    q = clean(row["text"])

    if len(q) < 15 or len(q) > 200:
        continue

    # remove system probing
    if any(b in q for b in BLOCK):
        continue

    # remove attack-like
    if any(a in q for a in ATTACK):
        continue

    # remove weak
    if any(q.startswith(w) for w in WEAK):
        continue

    # dedup
    if q in seen:
        continue

    seen.add(q)
    normal.append(q)

    if len(normal) >= 1500:
        break

print("OA normal collected:", len(normal))

# -------------------------------
# FORMAT
# -------------------------------
data = [{"query": q, "category": "normal"} for q in normal]

# -------------------------------
# SAVE
# -------------------------------
output_path = r"E:\llm-security-project\output\oa_normal.json"

with open(output_path, "w") as f:
    json.dump(data, f, indent=2)

print("Saved successfully at:", output_path)