import pandas as pd

# Define the rules manually (Expert Knowledge)
# We use columns: RuleID, Feature1, Operator1, Value1, Feature2, Operator2, Value2, Result, ResultValue
rules_data = [
    # --- LEVEL 1 RULES: Convert Numbers to Concepts ---
    ["R1", "Glucose", ">", 140, "None", "None", "None", "glucose_status", "High"],
    ["R2", "Glucose", "<=", 140, "None", "None", "None", "glucose_status", "Normal"],
    ["R3", "BMI", ">", 30, "None", "None", "None", "weight_status", "Obese"],
    ["R4", "BMI", "<=", 30, "None", "None", "None", "weight_status", "NotObese"],
    ["R5", "Age", ">", 50, "None", "None", "None", "age_group", "Senior"],
    ["R6", "BloodPressure", ">", 90, "None", "None", "None", "bp_status", "High"],
    
    # --- LEVEL 2 RULES: Chaining (Using concepts to find Risk) ---
    ["R7", "glucose_status", "==", "High", "weight_status", "==", "Obese", "risk_factor", "High"],
    ["R8", "glucose_status", "==", "High", "age_group", "==", "Senior", "risk_factor", "High"],
    ["R9", "glucose_status", "==", "Normal", "weight_status", "==", "NotObese", "risk_factor", "Low"],
    
    # --- LEVEL 3 RULES: Final Diagnosis (Outcome) ---
    # If Risk is High AND BP is High -> Diabetic
    ["R10", "risk_factor", "==", "High", "bp_status", "==", "High", "Outcome", 1],
    # If Risk is High (simple fallback) -> Diabetic
    ["R11", "risk_factor", "==", "High", "None", "None", "None", "Outcome", 1],
    # If Risk is Low -> Not Diabetic
    ["R12", "risk_factor", "==", "Low", "None", "None", "None", "Outcome", 0]
]

columns = ["RuleID", "Cond1", "Op1", "Val1", "Cond2", "Op2", "Val2", "Result_Attr", "Result_Val"]
df_rules = pd.DataFrame(rules_data, columns=columns)

# Save to CSV
df_rules.to_csv("diabetes_rules.csv", index=False)
print("diabetes_rules.csv created successfully!")