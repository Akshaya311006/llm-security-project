import json
import random

# -------------------------------
# LOAD FILES
# -------------------------------
with open(r"E:\llm-security-project\output\risk_data.json") as f:
    main_data = json.load(f)

with open(r"E:\llm-security-project\output\deepset_combined.json") as f:
    deep_data = json.load(f)

with open(r"E:\llm-security-project\output\hh_ambiguous.json") as f:
    hh_data = json.load(f)

print("Main:", len(main_data))
print("Deepset:", len(deep_data))
print("HH:", len(hh_data))


# -------------------------------
# MERGE
# -------------------------------
all_data = main_data + deep_data + hh_data

print("Before dedup:", len(all_data))


# -------------------------------
# REMOVE DUPLICATES
# -------------------------------
seen = set()
unique = []

for item in all_data:
    q = item["query"]
    if q not in seen:
        seen.add(q)
        unique.append(item)

print("After dedup:", len(unique))


# -------------------------------
# SHUFFLE
# -------------------------------
random.shuffle(unique)


# -------------------------------
# SAVE FINAL DATASET
# -------------------------------
with open(r"E:\llm-security-project\output\final_security_dataset.json", "w") as f:
    json.dump(unique, f, indent=2)

print("Final dataset saved successfully!")