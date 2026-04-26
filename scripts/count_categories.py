# import json

# # load final dataset
# with open(r"E:\llm-security-project\output\final_security_dataset.json") as f:
#     data = json.load(f)

# # counters
# counts = {
#     "prompt_injection": 0,
#     "ambiguous": 0
# }

# for item in data:
#     cat = item["category"]
#     if cat in counts:
#         counts[cat] += 1

# # print results
# print("Total:", len(data))
# print("Prompt Injection:", counts["prompt_injection"])
# print("Ambiguous:", counts["ambiguous"])

import json
from collections import Counter

# load final dataset
with open(r"E:\llm-security-project\output\final_dataset_final.json") as f:
    data = json.load(f)

# count categories
counts = Counter([item["category"] for item in data])

print("Total:", len(data))
print("Category distribution:")
for k, v in counts.items():
    print(k, ":", v)    