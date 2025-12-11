import tkinter as tk
from tkinter import messagebox
from inference_engine import load_rules, run_expert_system

def diagnose():
    try:
        # 1. Get Inputs from GUI
        user_data = {
            "Glucose": float(entry_glucose.get()),
            "BMI": float(entry_bmi.get()),
            "Age": float(entry_age.get()),
            "BloodPressure": float(entry_bp.get())
        }
        
        # 2. Run Engine
        rules = load_rules()
        final_facts, log = run_expert_system(user_data, rules)
        
        # 3. Show Result
        result_text = "--- Reasoning Steps ---\n" + "\n".join(log) + "\n\n"
        
        if "Outcome" in final_facts:
            outcome = "Positive (Diabetes)" if final_facts['Outcome'] == 1 else "Negative (Healthy)"
            result_text += f"FINAL DIAGNOSIS: {outcome}"
            lbl_result.config(fg="red" if final_facts['Outcome'] == 1 else "green")
        else:
            result_text += "Result: Inconclusive (No rule matched)"
            lbl_result.config(fg="black")
            
        lbl_result.config(text=result_text)
        
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers.")

# --- GUI SETUP ---
root = tk.Tk()
root.title("Diabetes Expert System")
root.geometry("400x500")

tk.Label(root, text="Diabetes Diagnosis Tool", font=("Arial", 14, "bold")).pack(pady=10)

# Input Fields
tk.Label(root, text="Glucose Level:").pack()
entry_glucose = tk.Entry(root)
entry_glucose.pack()

tk.Label(root, text="BMI:").pack()
entry_bmi = tk.Entry(root)
entry_bmi.pack()

tk.Label(root, text="Age:").pack()
entry_age = tk.Entry(root)
entry_age.pack()

tk.Label(root, text="Blood Pressure:").pack()
entry_bp = tk.Entry(root)
entry_bp.pack()

# Button
tk.Button(root, text="Analyze Patient", command=diagnose, bg="lightblue").pack(pady=20)

# Output
lbl_result = tk.Label(root, text="Waiting for input...", justify="left", wraplength=350)
lbl_result.pack()

root.mainloop()