import json
import random

# -------------------------------
# 1. FILE PATHS (EDIT IF NEEDED)
# -------------------------------
REAL_DATA_PATH = r"E:\llm-security-project\output\risk_data.json"
SYNTHETIC_DATA_PATH = r"E:\llm-security-project\output\clean_prompt_injection.json"
OUTPUT_PATH = r"E:\llm-security-project\output\final_prompt_injection_dataset.json"


# -------------------------------
# 2. LOAD DATA
# -------------------------------
with open(REAL_DATA_PATH, "r") as f:
    real_data = json.load(f)

with open(SYNTHETIC_DATA_PATH, "r") as f:
    synthetic_data = json.load(f)

print("Real data:", len(real_data))
print("Synthetic data:", len(synthetic_data))


# -------------------------------
# 3. REMOVE DUPLICATES
# -------------------------------
real_set = set(item["query"].lower() for item in real_data)

filtered_synthetic = [
    item for item in synthetic_data
    if item["query"].lower() not in real_set
]

print("Synthetic after dedup:", len(filtered_synthetic))


# -------------------------------
# 4. LIMIT SYNTHETIC (30%)
# -------------------------------
MAX_SYNTHETIC = int(len(real_data) * 0.3)

if len(filtered_synthetic) > MAX_SYNTHETIC:
    filtered_synthetic = filtered_synthetic[:MAX_SYNTHETIC]

print("Synthetic used:", len(filtered_synthetic))


# -------------------------------
# 5. MERGE DATA
# -------------------------------
final_data = real_data + filtered_synthetic

print("Total before shuffle:", len(final_data))


# -------------------------------
# 6. SHUFFLE (IMPORTANT)
# -------------------------------
random.shuffle(final_data)


# -------------------------------
# 7. FINAL CHECK (OPTIONAL)
# -------------------------------
queries = [item["query"].lower() for item in final_data]
print("Final unique queries:", len(set(queries)))


# -------------------------------
# 8. SAVE FINAL DATASET
# -------------------------------
with open(OUTPUT_PATH, "w") as f:
    json.dump(final_data, f, indent=2)

print("Final dataset saved successfully!")