import pandas as pd
from inference_engine import load_rules, run_expert_system

def calculate_metrics(y_true, y_pred):
    """
    Calculates classification metrics from scratch without ML libraries.
    """
    tp = 0 # True Positive
    tn = 0 # True Negative
    fp = 0 # False Positive
    fn = 0 # False Negative
    unclassified = 0

    for true, pred in zip(y_true, y_pred):
        if pred == -1: # Our code for "No Rule Matched"
            unclassified += 1
            continue
            
        if true == 1 and pred == 1:
            tp += 1
        elif true == 0 and pred == 0:
            tn += 1
        elif true == 0 and pred == 1:
            fp += 1
        elif true == 1 and pred == 0:
            fn += 1

    # avoid division by zero
    accuracy = (tp + tn) / len(y_true) if len(y_true) > 0 else 0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    return {
        "TP": tp, "TN": tn, "FP": fp, "FN": fn, "Unclassified": unclassified,
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1_Score": f1
    }

def main():
    # 1. Load Data and Rules
    print("Loading data and rules...")
    df = pd.read_csv("diabetes.csv")
    rules = load_rules("diabetes_rules.csv")

    y_true = []
    y_pred = []

    print(f"Running Expert System on {len(df)} patients...")

    # 2. Iterate through the whole dataset
    for index, row in df.iterrows():
        # Prepare input data
        patient_data = row.to_dict()
        
        # Get the actual truth
        actual_outcome = int(row['Outcome'])
        y_true.append(actual_outcome)

        # Run our Rule-Based Engine
        # We don't need the logs (trace) here, just the facts
        facts, _ = run_expert_system(patient_data, rules)

        # 3. Determine Prediction
        if 'Outcome' in facts:
            prediction = int(facts['Outcome'])
        else:
            # If our rules were too strict and didn't fire, we mark as -1
            prediction = -1 
        
        y_pred.append(prediction)

    # 4. Calculate Metrics
    m = calculate_metrics(y_true, y_pred)

    # 5. Print "Classification Report"
    print("\n" + "="*40)
    print("   RULE-BASED SYSTEM PERFORMANCE REPORT")
    print("="*40)
    print(f"Total Samples Processed: {len(df)}")
    print(f"Unclassified (No Rule Fired): {m['Unclassified']}")
    print("-" * 40)
    print(f"True Positives  (Hit):  {m['TP']}")
    print(f"True Negatives  (Hit):  {m['TN']}")
    print(f"False Positives (Miss): {m['FP']}")
    print(f"False Negatives (Miss): {m['FN']}")
    print("-" * 40)
    print(f"ACCURACY:  {m['Accuracy']:.2%}")
    print(f"PRECISION: {m['Precision']:.2%}")
    print(f"RECALL:    {m['Recall']:.2%}")
    print(f"F1 SCORE:  {m['F1_Score']:.4f}")
    print("="*40)
    print("\nInterpreting the results:")
    print("- Low Recall? Your rules for detecting Diabetes (Class 1) are too strict.")
    print("- Low Precision? Your rules are diagnosing healthy people as diabetic too often.")
    print("- High Unclassified? Your rules don't cover enough ranges (gaps in logic).")

if __name__ == "__main__":
    main()