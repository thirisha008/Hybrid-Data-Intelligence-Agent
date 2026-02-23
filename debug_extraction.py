import pandas as pd
import sys
sys.path.insert(0, ".")
from csv_reader import ControlledDataAssistant

# Test extraction functions
assistant = ControlledDataAssistant()
assistant.df = pd.read_csv("dataset.csv.csv")

questions = [
    "give the reviewcount of Shri Vetrivel IT Care",
    "what is the phone of IT Konnect"
]

for q in questions:
    print(f"\n{'='*70}")
    print(f"Question: {q}")
    print(f"{'='*70}")
    
    company = assistant.extract_company_name(q)
    print(f"Extracted Company: '{company}'")
    
    metric = assistant.extract_metric(q)
    print(f"Extracted Metric: {metric}")
    
    result = assistant.search_company(company)
    if result:
        row, idx = result
        print(f"Found: '{row['title']}' at Row {idx + 1}")
        if metric:
            print(f"Value: {row.get(metric, 'NOT FOUND')}")
    else:
        print("Company not found")
