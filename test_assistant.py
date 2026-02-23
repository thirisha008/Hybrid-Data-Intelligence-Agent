import pandas as pd
import logging
import sys

# Setup logging
logging.basicConfig(
    filename="agent.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Import the assistant class
sys.path.insert(0, ".")
from csv_reader import ControlledDataAssistant

# Create assistant and load CSV
assistant = ControlledDataAssistant()
assistant.df = pd.read_csv("dataset.csv.csv")
assistant.csv_path = "dataset.csv.csv"

print("✅ CSV Loaded Successfully!")
print(f"📊 Rows: {len(assistant.df)}, Columns: {len(assistant.df.columns)}\n")

# Test cases
test_questions = [
    "give the reviewcount of Shri Vetrivel IT Care",
    "tell about Shri Vetrivel IT Care",
    "what is the phone of IT Konnect",
    "IT Konnect address",
    "how many rows in the dataset"
]

print("="*70)
print("TESTING CONTROLLED DATA ASSISTANT")
print("="*70)

for question in test_questions:
    print(f"\n❓ Question: {question}")
    print("-" * 70)
    
    # Try company question first
    company_result = assistant.answer_company_question(question)
    if company_result:
        pass
    # Try data question
    elif assistant.is_data_question(question):
        assistant.answer_data_question(question)
    else:
        print("⚠️ Question not recognized")
    
    print()


