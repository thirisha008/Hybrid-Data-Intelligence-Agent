import pandas as pd
import sys
sys.path.insert(0, ".")
from csv_reader import ControlledDataAssistant

# Create assistant and load CSV
assistant = ControlledDataAssistant()
assistant.df = pd.read_csv("dataset.csv.csv")
assistant.csv_path = "dataset.csv.csv"

print("✅ CSV Loaded Successfully!")
print(f"📊 Rows: {len(assistant.df)}, Columns: {len(assistant.df.columns)}\n")

# Test address search
test_question = "which company is located in 547, Dr Rajendra Prasad Rd, opposite to RISHABA POLY PACKS, Coimbatore"

print("="*70)
print("TESTING IMPROVED ADDRESS SEARCH")
print("="*70)
print(f"\n❓ Question: {test_question}")
print("-" * 70)

# Check if it's an address question
if assistant.is_address_question(test_question):
    print("[DEBUG] Identified as address question")
    result = assistant.search_by_address(test_question)
    if not result:
        print("No results from smart search")
else:
    print("[DEBUG] Not identified as address question")
