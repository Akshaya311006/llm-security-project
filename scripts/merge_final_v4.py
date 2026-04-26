import json
import random

# -------------------------------
# LOAD ALL DATASETS
# -------------------------------

with open(r"E:\llm-security-project\output\final_security_dataset_refined.json") as f:
    main_data = json.load(f)

with open(r"E:\llm-security-project\output\normal_data.json") as f:
    normal_data = json.load(f)

with open(r"E:\llm-security-project\output\ambiguous_expanded.json") as f:
    amb_old = json.load(f)

with open(r"E:\llm-security-project\output\openassistant_ambiguous.json") as f:
    oa_amb = json.load(f)

with open(r"E:\llm-security-project\output\hh_ambiguous_expanded.json") as f:
    hh_amb = json.load(f)

# optional synthetic ambiguous (keep if you want)
with open(r"E:\llm-security-project\output\ambiguous_synthetic.json") as f:
    amb_syn = json.load(f)

# -------------------------------
# NEW NORMAL DATASETS (IMPORTANT)
# -------------------------------
with open(r"E:\llm-security-project\output\alpaca_normal.json") as f:
    alpaca_normal = json.load(f)

with open(r"E:\llm-security-project\output\dolly_normal.json") as f:
    dolly_normal = json.load(f)

with open(r"E:\llm-security-project\output\oa_normal.json") as f:
    oa_normal = json.load(f)

print("Alpaca normal:", len(alpaca_normal))
print("Dolly normal:", len(dolly_normal))
print("OA normal:", len(oa_normal))

print("Synthetic ambiguous:", len(amb_syn))
print("Main:", len(main_data))
print("Normal:", len(normal_data))
print("Ambiguous old:", len(amb_old))
print("OpenAssistant:", len(oa_amb))
print("HH:", len(hh_amb))


# -------------------------------
# MERGE ALL
# -------------------------------
all_data = (
    main_data +
    normal_data +
    amb_old +
    oa_amb +
    hh_amb +
    amb_syn +
    alpaca_normal +
    dolly_normal +
    oa_normal
)

print("Before dedup:", len(all_data))


# -------------------------------
# REMOVE DUPLICATES (PRIORITY)
# -------------------------------
priority = {
    "prompt_injection": 3,
    "ambiguous": 2,
    "normal": 1
}

data_map = {}

for item in all_data:
    q = item["query"].strip().lower()
    cat = item["category"]

    if q not in data_map:
        data_map[q] = cat
    else:
        if priority.get(cat, 0) > priority.get(data_map[q], 0):
            data_map[q] = cat

# convert back
unique = [{"query": q, "category": c} for q, c in data_map.items()]

print("After dedup:", len(unique))


# -------------------------------
# OPTIONAL BALANCING (RECOMMENDED)
# -------------------------------
ambiguous = [x for x in unique if x["category"] == "ambiguous"]
injection = [x for x in unique if x["category"] == "prompt_injection"]
normal = [x for x in unique if x["category"] == "normal"]

print("Before balance:",
      "ambiguous:", len(ambiguous),
      "injection:", len(injection),
      "normal:", len(normal))

# you said you want 5000 normal
ambiguous = ambiguous[:5000]
injection = injection[:3500]
normal = normal[:5000]

final_data = ambiguous + injection + normal

print("After balance:",
      "ambiguous:", len(ambiguous),
      "injection:", len(injection),
      "normal:", len(normal))


# -------------------------------
# SHUFFLE
# -------------------------------
random.shuffle(final_data)


# -------------------------------
# SAVE FINAL DATASET
# -------------------------------
output_path = r"E:\llm-security-project\output\final_dataset_final.json"

with open(output_path, "w") as f:
    json.dump(final_data, f, indent=2)

print("Saved successfully at:", output_path)