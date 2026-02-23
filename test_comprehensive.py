import pandas as pd
import sys
import logging

sys.path.insert(0, ".")
from csv_reader import ControlledDataAssistant

# Create assistant and load CSV
assistant = ControlledDataAssistant()
assistant.df = pd.read_csv("dataset.csv.csv")
assistant.csv_path = "dataset.csv.csv"

print("✅ CSV Loaded Successfully!")
print(f"📊 Rows: {len(assistant.df)}, Columns: {len(assistant.df.columns)}\n")

# Test cases
test_cases = [
    ("which company is located in 547, Dr Rajendra Prasad Rd, opposite to RISHABA POLY PACKS, Coimbatore", "address"),
    ("give the reviewcount of Shri Vetrivel IT Care", "company_metric"),
    ("tell about IT Konnect", "company_full"),
    ("how many rows in the dataset", "data_aggregation"),
]

print("="*70)
print("COMPREHENSIVE ASSISTANT TESTING WITH ENHANCED LOGGING")
print("="*70)

for question, test_type in test_cases:
    print(f"\n❓ [{test_type}] {question}")
    print("-" * 70)
    
    # Check question type
    if assistant.is_address_question(question):
        assistant.search_by_address(question)
    elif assistant.answer_company_question(question):
        pass
    elif assistant.is_data_question(question):
        assistant.answer_data_question(question)
    else:
        print("⚠️ Could not process question")
    
    print()

# Check logs
print("\n" + "="*70)
print("CHECKING LOG FILE")
print("="*70)
print("\nReading agent.log (last 40 lines):\n")

try:
    with open("agent.log", "r") as f:
        lines = f.readlines()
        for line in lines[-40:]:
            print(line.rstrip())
except Exception as e:
    print(f"Could not read log file: {e}")
