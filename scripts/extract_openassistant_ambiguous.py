import json
from datasets import load_dataset

def clean(q):
    return " ".join(str(q).lower().strip().split())

print("Loading OpenAssistant dataset...")

# load normally (NOT streaming → easier debugging)
ds = load_dataset("OpenAssistant/oasst1", split="train")

print("Total rows:", len(ds))

# -------------------------------
# FILTER SETTINGS
# -------------------------------

AMB_STRONG = [
    "system", "rules", "policy", "behavior",
    "limitations", "model", "training",
    "how do you", "how does your",
    "what are your", "explain your",
    "internal"
]

SAFE_PATTERNS = [
    "write a poem", "tell me a joke", "translate",
    "summarize", "paraphrase", "solve",
    "calculate", "generate", "create"
]

ATTACK_PATTERNS = [
    "ignore previous instructions", "bypass",
    "override", "reveal system prompt",
    "developer mode", "jailbreak"
]

# -------------------------------
# EXTRACT
# -------------------------------
ambiguous = []
seen = set()

for i, row in enumerate(ds):

    # progress print
    if i % 5000 == 0:
        print("Processed:", i)

    # only user messages
    if row["role"] != "prompter":
        continue

    q = clean(row.get("text", ""))

    if len(q) < 15 or len(q) > 300:
        continue

    # keep ambiguous-type
    if not any(k in q for k in AMB_STRONG) and not (
    ("how" in q or "what" in q or "why" in q)
    and ("model" in q or "system" in q or "rules" in q or "behavior" in q)
):
        continue

    # remove safe
    if any(s in q for s in SAFE_PATTERNS):
        continue

    # remove strong attacks
    if any(a in q for a in ATTACK_PATTERNS):
        continue

    # deduplicate
    if q in seen:
        continue

    seen.add(q)
    ambiguous.append(q)

    # limit
    if len(ambiguous) >= 1500:
        break

print("Collected ambiguous:", len(ambiguous))

# -------------------------------
# FORMAT
# -------------------------------
data = [{"query": q, "category": "ambiguous"} for q in ambiguous]

# -------------------------------
# SAVE
# -------------------------------
output_path = r"E:\llm-security-project\output\openassistant_ambiguous.json"

with open(output_path, "w") as f:
    json.dump(data, f, indent=2)

print("Saved successfully at:", output_path)