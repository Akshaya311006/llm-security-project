import json
from datasets import load_dataset

def clean(q):
    return " ".join(str(q).lower().strip().split())

print("Loading HH dataset...")

# load HH dataset
ds = load_dataset("Anthropic/hh-rlhf", split="train")

print("Total rows:", len(ds))

# -------------------------------
# FILTER SETTINGS
# -------------------------------

# strong ambiguous signals
AMB_STRONG = [
    "how do you", "how does your", "how are you",
    "what are your", "explain your", "internal",
    "system", "rules", "policy", "behavior",
    "limitations", "model", "training"
]

# remove safe queries
SAFE_PATTERNS = [
    "write a poem", "tell me a joke", "translate",
    "summarize", "calculate", "code", "generate",
    "create", "solve", "story"
]

# remove attack queries
ATTACK_PATTERNS = [
    "ignore previous instructions", "bypass",
    "override", "reveal system prompt",
    "developer mode", "jailbreak"
]

ambiguous = []
seen = set()

# -------------------------------
# EXTRACT
# -------------------------------
for i, row in enumerate(ds):

    if i % 5000 == 0:
        print("Processed:", i)

    # extract human prompt
    text = row.get("chosen", "")

    # split conversation → take first human part
    if "Human:" in text:
        q = text.split("Human:")[1].split("Assistant:")[0]
    else:
        continue

    q = clean(q)

    if len(q) < 15 or len(q) > 300:
        continue

    # keep ambiguous
    if not any(k in q for k in AMB_STRONG) and not (
    ("how" in q or "what" in q or "why" in q)
    and len(q) > 20
):
        continue

    # remove safe
    if any(s in q for s in SAFE_PATTERNS):
        continue

    # remove attack
    if any(a in q for a in ATTACK_PATTERNS):
        continue

    # deduplicate
    if q in seen:
        continue

    seen.add(q)
    ambiguous.append(q)

    # limit
    if len(ambiguous) >= 4000:
        break

print("Collected ambiguous:", len(ambiguous))

# -------------------------------
# FORMAT
# -------------------------------
data = [{"query": q, "category": "ambiguous"} for q in ambiguous]

# -------------------------------
# SAVE
# -------------------------------
output_path = r"E:\llm-security-project\output\hh_ambiguous_expanded.json"

with open(output_path, "w") as f:
    json.dump(data, f, indent=2)

print("Saved successfully at:", output_path)