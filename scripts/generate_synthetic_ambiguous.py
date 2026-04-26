import json
import random

# -------------------------------
# LOAD EXISTING DATA (for dedup)
# -------------------------------
with open(r"E:\llm-security-project\output\final_dataset_v4.json") as f:
    existing = json.load(f)

existing_set = set([item["query"].strip().lower() for item in existing])

print("Existing dataset:", len(existing_set))


# -------------------------------
# TEMPLATES (diverse ambiguous)
# -------------------------------

templates = [
    "how does your system decide {x}",
    "what factors influence {x}",
    "can you explain how your model handles {x}",
    "what rules guide your behavior when {x}",
    "how are decisions made internally for {x}",
    "what limitations affect your responses to {x}",
    "how does your model process {x}",
    "what internal mechanisms handle {x}",
    "how do you determine outcomes for {x}",
    "what constraints influence your answers about {x}",
]

topics = [
    "user queries",
    "complex questions",
    "uncertain inputs",
    "ambiguous requests",
    "edge cases",
    "sensitive topics",
    "policy-related questions",
    "unknown scenarios",
    "conflicting instructions",
    "multi-step reasoning",
]

# -------------------------------
# GENERATE SYNTHETIC
# -------------------------------
synthetic = []
seen = set()

TARGET = 800  # safe range

while len(synthetic) < TARGET:

    t = random.choice(templates)
    topic = random.choice(topics)

    q = t.format(x=topic).strip().lower()

    # remove duplicates (existing + new)
    if q in existing_set or q in seen:
        continue

    seen.add(q)

    synthetic.append({
        "query": q,
        "category": "ambiguous"
    })

print("Generated synthetic:", len(synthetic))


# -------------------------------
# SAVE
# -------------------------------
output_path = r"E:\llm-security-project\output\synthetic_ambiguous.json"

with open(output_path, "w") as f:
    json.dump(synthetic, f, indent=2)

print("Saved successfully at:", output_path)