#!/usr/bin/env python3
"""Test the fixes for company name extraction and address search"""

import pandas as pd

# Load the CSV
df = pd.read_csv('dataset.csv.csv')

def test_company_extraction():
    """Test if company name extraction works correctly"""
    print("="*70)
    print("TEST 1: COMPANY NAME EXTRACTION FIX")
    print("="*70)
    
    # Test case 1: "give the details of TricKey Smart IT Solution"
    question = "give the details of TricKey Smart IT Solution"
    q = question.lower()
    
    phrases_to_remove = [
        "tell me about", "tell about", "what about", "info on", "details of", "details on",
        "give me", "give the", "what is the", "what is", "find", "show", "which",
        "company", "the", "of the", "for the", "of "
    ]
    
    # Sort by length (longest first)
    phrases_to_remove = sorted(phrases_to_remove, key=len, reverse=True)
    
    for phrase in phrases_to_remove:
        q = q.replace(phrase, " ").strip()
    
    q = q.replace("?", "").replace("'s", "").replace('"', "").replace("'", "").strip()
    q = " ".join(q.split())
    
    print(f"\nTest question: {question}")
    print(f"Extracted company name: '{q}'")
    
    # Search for it
    matches = df[df['title'].astype(str).str.lower().str.contains(q, na=False)]
    if not matches.empty:
        print(f"✅ FOUND! Matched company: {matches.iloc[0]['title']}")
        print(f"   Address: {matches.iloc[0]['street']}, {matches.iloc[0]['city']}")
    else:
        print(f"❌ NOT FOUND")
    
    print()

def test_address_search():
    """Test if address search works correctly"""
    print("="*70)
    print("TEST 2: ADDRESS SEARCH FIX")
    print("="*70)
    
    # Test case: Finding company at "2nd Floor", "Gandhipuram, Coimbatore"
    question = 'give the name of the company which is located at 2nd Floor","Gandhipuram, Coimbatore'
    keywords = question.lower()
    
    # Remove common question words/phrases that don't contribute to address search
    remove_words = [
        "which company", "what company", "give me", "give the",
        "name of", "names of", "is located at", "located at", "is located in", 
        "located in", "tell me about", "tell about", "info on", "details of",
        "which", "is", "the", "of", "a", "an"
    ]
    
    # Sort by length (longest first)
    remove_words = sorted(remove_words, key=len, reverse=True)
    
    for word in remove_words:
        keywords = keywords.replace(" " + word + " ", " ")
        # Also remove from start/end
        if keywords.startswith(word + " "):
            keywords = keywords[len(word)+1:]
        if keywords.endswith(" " + word):
            keywords = keywords[:-len(word)-1]
    
    keywords = keywords.replace('"', "").replace("'", "").replace("``", "").replace("'", "")
    keywords = keywords.replace("?", "").replace(",", " ").strip()
    keywords = " ".join(keywords.split())
    
    print(f"\nTest question: {question}")
    print(f"Extracted keywords: '{keywords}'")
    
    # Search logic - similar to what csv_reader does
    terms = [t.strip().lower() for t in keywords.split(',')]
    terms = [t for t in terms if t]  # Remove empty terms
    
    # If no comma-split terms, just use the full string as single term
    if len(terms) == 1:
        terms = keywords.split()
    
    print(f"Search terms: {terms}")
    
    # Find rows that match ALL terms
    mask = pd.Series([True] * len(df))
    
    for term in terms:
        if term:
            term_mask = pd.Series([False] * len(df))
            for col in df.columns:
                col_lower = df[col].astype(str).str.lower()
                col_term_mask = col_lower.str.contains(term, na=False)
                term_mask = term_mask | col_term_mask
            
            mask = mask & term_mask
    
    matching_rows = df[mask]
    
    if not matching_rows.empty:
        print(f"\n✅ FOUND {len(matching_rows)} matching company(ies):")
        for idx, row in matching_rows.iterrows():
            print(f"   Company: {row['title']}")
            print(f"   Address: {row['street']}, {row['city']}")
    else:
        print(f"\n❌ NO MATCHES FOUND")
    
    print()

if __name__ == "__main__":
    test_company_extraction()
    test_address_search()
    print("="*70)
    print("TESTS COMPLETED")
    print("="*70)
