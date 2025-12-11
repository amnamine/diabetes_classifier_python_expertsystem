# Create a separate test_script.py
import pandas as pd
from inference_engine import load_rules, run_expert_system

# Load real data
df = pd.read_csv("diabetes.csv").head(5) # Test first 5 patients
rules = load_rules()

print("--- BATCH TESTING ---")
for index, row in df.iterrows():
    # Convert row to dict
    patient_data = row.to_dict()
    
    # Run System
    facts, _ = run_expert_system(patient_data, rules)
    
    # Compare
    predicted = facts.get('Outcome', 'Unknown')
    actual = row['Outcome']
    print(f"Patient {index}: Predicted={predicted}, Actual={actual}")