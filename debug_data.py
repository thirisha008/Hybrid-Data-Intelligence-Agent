import pandas as pd

# Load CSV and search manually
df = pd.read_csv("dataset.csv.csv")

print("Searching for 'rajendra prasad' in all columns:")
print("="*70)

# Search for the address
search_term = "rajendra prasad"

# Create a mask by checking each column separately
mask = pd.Series([False] * len(df))
for col in df.columns:
    col_lower = df[col].astype(str).str.lower()
    col_mask = col_lower.str.contains(search_term, na=False)
    mask = mask | col_mask

matches = df[mask]

print(f"\nFound {len(matches)} matches\n")

if not matches.empty:
    for idx, row in matches.iterrows():
        print(f"Row {idx + 1}:")
        print(f"  Title: {row['title']}")
        print(f"  Street: {row['street']}")
        print(f"  City: {row['city']}")
        print(f"  Phone: {row['phone']}")
        print()

print("\n" + "="*70)
print("Also checking for '547' anywhere in the data:")
print("="*70)

search_term2 = "547"

# Search again for 547
mask2 = pd.Series([False] * len(df))
for col in df.columns:
    col_lower = df[col].astype(str).str.lower()
    col_mask = col_lower.str.contains(search_term2, na=False)
    mask2 = mask2 | col_mask

matches2 = df[mask2]

print(f"\nFound {len(matches2)} matches\n")

if not matches2.empty:
    for idx, row in matches2.iterrows():
        print(f"Row {idx + 1}:")
        print(f"  Title: {row['title']}")
        print(f"  Street: {row['street']}")
        print()
