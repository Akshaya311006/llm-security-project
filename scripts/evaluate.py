import json
from collections import defaultdict

# -------------------------------
# IMPORT ANALYZER FUNCTION
# -------------------------------
from input_analyzer import analyze_query


# -------------------------------
# LOAD DATASET
# -------------------------------
with open(r"E:\llm-security-project\output\final_dataset_v2.json") as f:
    data = json.load(f)

print("Dataset size:", len(data))


# -------------------------------
# INITIALIZE METRICS
# -------------------------------
correct = 0
total = len(data)

# confusion matrix
conf_matrix = defaultdict(lambda: defaultdict(int))

categories = ["prompt_injection", "ambiguous", "normal"]

# -------------------------------
# RUN EVALUATION
# -------------------------------
for item in data:
    true_label = item["category"]
    query = item["query"]

    result = analyze_query(query)
    pred_label = result["category"]

    # accuracy
    if true_label == pred_label:
        correct += 1

    # confusion matrix
    conf_matrix[true_label][pred_label] += 1


# -------------------------------
# ACCURACY
# -------------------------------
accuracy = correct / total
print("\nAccuracy:", round(accuracy, 4))


# -------------------------------
# PRINT CONFUSION MATRIX
# -------------------------------
print("\nConfusion Matrix:")
print("Actual \\ Predicted")

for actual in categories:
    row = []
    for pred in categories:
        row.append(conf_matrix[actual][pred])
    print(f"{actual:20} {row}")


# -------------------------------
# PRECISION & RECALL
# -------------------------------
print("\nPrecision & Recall:")

for cat in categories:
    tp = conf_matrix[cat][cat]
    fp = sum(conf_matrix[other][cat] for other in categories if other != cat)
    fn = sum(conf_matrix[cat][other] for other in categories if other != cat)

    precision = tp / (tp + fp) if (tp + fp) != 0 else 0
    recall = tp / (tp + fn) if (tp + fn) != 0 else 0

    print(f"{cat}: Precision={round(precision,3)} Recall={round(recall,3)}")