# import json
# import random

# # -------------------------------
# # LOAD EXISTING DATA (injection + ambiguous)
# # -------------------------------
# with open(r"E:\llm-security-project\output\final_security_dataset_refined.json") as f:
#     main_data = json.load(f)

# print("Main dataset:", len(main_data))


# # -------------------------------
# # LOAD NORMAL DATA
# # -------------------------------
# with open(r"E:\llm-security-project\output\normal_data.json") as f:
#     normal_data = json.load(f)

# print("Normal dataset:", len(normal_data))


# # -------------------------------
# # MERGE
# # -------------------------------
# all_data = main_data + normal_data

# print("Before dedup:", len(all_data))


# # -------------------------------
# # REMOVE DUPLICATES
# # -------------------------------
# seen = set()
# unique = []

# for item in all_data:
#     q = item["query"].strip().lower()

#     if q not in seen:
#         seen.add(q)
#         unique.append({
#             "query": q,
#             "category": item["category"]
#         })

# print("After dedup:", len(unique))


# # -------------------------------
# # SHUFFLE DATA
# # -------------------------------
# random.shuffle(unique)


# # -------------------------------
# # SAVE FINAL DATASET
# # -------------------------------
# output_path = r"E:\llm-security-project\output\final_dataset_v2.json"

# with open(output_path, "w") as f:
#     json.dump(unique, f, indent=2)

# print("Saved successfully at:", output_path)

import json
import random

# -------------------------------
# LOAD MAIN DATA (old injection + ambiguous)
# -------------------------------
with open(r"E:\llm-security-project\output\final_security_dataset_refined.json") as f:
    main_data = json.load(f)

print("Main dataset:", len(main_data))


# -------------------------------
# LOAD NORMAL DATA
# -------------------------------
with open(r"E:\llm-security-project\output\normal_data.json") as f:
    normal_data = json.load(f)

print("Normal dataset:", len(normal_data))


# -------------------------------
# LOAD EXPANDED AMBIGUOUS
# -------------------------------
with open(r"E:\llm-security-project\output\ambiguous_expanded.json") as f:
    amb_expanded = json.load(f)

print("Expanded ambiguous:", len(amb_expanded))


# -------------------------------
# MERGE ALL
# -------------------------------
all_data = main_data + normal_data + amb_expanded

print("Before dedup:", len(all_data))


# -------------------------------
# REMOVE DUPLICATES
# -------------------------------
seen = set()
unique = []

for item in all_data:
    q = item["query"].strip().lower()

    if q not in seen:
        seen.add(q)
        unique.append({
            "query": q,
            "category": item["category"]
        })

print("After dedup:", len(unique))


# -------------------------------
# SHUFFLE
# -------------------------------
random.shuffle(unique)


# -------------------------------
# SAVE FINAL DATASET
# -------------------------------
output_path = r"E:\llm-security-project\output\final_dataset_v3.json"

with open(output_path, "w") as f:
    json.dump(unique, f, indent=2)

print("Saved successfully at:", output_path)