# Quick Start Guide - Controlled Data Assistant

## 🚀 Running the Assistant

### Option 1: Interactive Mode (Recommended)
```bash
cd c:\Users\THIRISHA\OneDrive\Desktop\New\ folder\Agents
python csv_reader.py
```

Then answer prompts:
```
Enter CSV file path: dataset.csv.csv

Your question: which company is located in 547, Dr Rajendra Prasad Rd, opposite to RISHABA POLY PACKS, Coimbatore
```

### Option 2: Quick Test
```bash
python test_comprehensive.py
```

### Option 3: Verify User's Question
```bash
python final_verification.py
```

---

## 📋 Question Examples & Results

### Address Search
```
Q: "which company is located in 547, Dr Rajendra Prasad Rd"
A: DIX IT STORE (Row 26)
   Address: 547, Dr Rajendra Prasad Rd, opposite to RISHABA POLY PACKS, Coimbatore, Tamil Nadu
```

### Company Metrics
```
Q: "give the reviewcount of Shri Vetrivel IT Care"
A: reviewsCount: 131.0 (Row 8)
```

### Company Full Details
```
Q: "tell about IT Konnect"
A: Full details including:
   - Phone: +91 74185 60077
   - Address: 74, 100 Feet Rd, Gandhipuram, Coimbatore
   - Website: https://itkonnect.in/
   - Categories: Computer service, repair, data recovery
```

### Data Aggregation
```
Q: "how many rows in the dataset"
A: Total rows: 140
```

---

## 📊 Viewing Logs

### See Recent Activity
```bash
tail agent.log
```

### See Full Debug Trace
```bash
cat agent.log
```

### Search Logs for Specific Query
```bash
grep "which company" agent.log
```

### See All DEBUG Messages
```bash
grep DEBUG agent.log
```

---

## 🔧 How It Works

```
┌─────────────────────────────────────┐
│        User Question                │
│ "which company is at 547..."        │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│   Question Type Detection           │
│   → "located" found = ADDRESS       │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│   Extract Keywords                  │
│   → "547, Dr Rajendra Prasad Rd..." │
│   → Clean quotes & spaces           │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│   Split into Search Terms           │
│   → ['547', 'dr rajendra...', ...] │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│   Progressive Filtering             │
│   Start: 140 rows                   │
│   After '547': 2 rows               │
│   After 'dr rajendra': 1 row    ✓   │
│   After 'opposite to': 1 row    ✓   │
│   After 'coimbatore': 1 row     ✓   │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│   Search CSV                        │
│   Found: DIX IT STORE (Row 26)      │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│   Return Result with CSV Reference  │
│   Row 26: DIX IT STORE              │
│   Address: 547, Dr Rajendra...      │
│   Phone: nan                        │
└─────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│   Log Every Step                    │
│   [INFO] Address search initiated   │
│   [DEBUG] Extracted keywords        │
│   [DEBUG] After filtering '547': 2  │
│   [INFO] Search returned 1 row      │
└─────────────────────────────────────┘
```

---

## ✅ Features Checklist

```
CSV Search:
  ✅ Address-based search
  ✅ Company lookup by name
  ✅ Metric extraction (phone, address, reviews, etc.)
  ✅ Data aggregation (count, sum, avg, max, min)

Data Transparency:
  ✅ Row number references
  ✅ Column names shown
  ✅ Sample data displayed
  ✅ Search methodology explained

Logging:
  ✅ DEBUG level (detailed traces)
  ✅ INFO level (key milestones)
  ✅ Function names logged
  ✅ Timestamps for every action
  ✅ Filter stage logging
  ✅ Results logged

Control Rules:
  ✅ RULE 1: Answers from CSV only
  ✅ RULE 2: Internet disabled by default
  ✅ RULE 3: Permission required for online
  ✅ RULE 4: Reasoning shown with references
  ✅ RULE 5: No fabrication/guessing
```

---

## 🐛 Troubleshooting

### Issue: "File not found"
**Solution:** Provide full path or ensure file is in current directory
```bash
# Good
Enter CSV file path: C:\Users\THIRISHA\OneDrive\Desktop\New folder\Agents\dataset.csv.csv

# Also works if in directory
Enter CSV file path: dataset.csv.csv
```

### Issue: Question not answered
**Solution:** Check logs to see what type was detected
```bash
# Check logs
grep "DEBUG" agent.log | tail -5

# Look for these messages:
# - "Address question check: True/False"
# - "Data question check: True/False"
# - "Company question detected"
```

### Issue: No matching results
**Solution:** Check if data exists in CSV
```bash
# Use debug script to search for data
python debug_data.py
```

---

## 📁 Files Reference

| File | Purpose |
|------|---------|
| `csv_reader.py` | Main assistant class - Run this for interactive mode |
| `test_comprehensive.py` | Tests all question types |
| `final_verification.py` | Tests your exact question |
| `debug_data.py` | Inspect CSV data manually |
| `agent.log` | Execution logs (auto-created) |
| `dataset.csv.csv` | IT companies data |
| `shopping_behavior_updated.csv` | Shopping behavior data |
| `SOLUTION_REPORT.md` | Complete technical report |
| `IMPROVEMENT_SUMMARY.md` | Feature documentation |

---

## 🎯 Key Points

1. **All answers come from CSV** - No assumptions, all data verified
2. **Comprehensive logging** - Every step traced with timestamps
3. **Row references** - Always shows which CSV row was used
4. **Smart search** - Understands natural language queries
5. **Permission-based** - Requires user consent for anything beyond CSV

---

## 🎓 Example Session

```
$ python csv_reader.py

✅ CSV Loaded Successfully!
📄 File: dataset.csv.csv
📊 Rows: 140, Columns: 21
📋 Columns: title, totalScore, reviewsCount, street, city, ...

============================================================
🤖 CONTROLLED DATA ASSISTANT (CSV-ONLY MODE)
============================================================

Your question: which company is located in 547, Dr Rajendra Prasad Rd, opposite to RISHABA POLY PACKS, Coimbatore

📍 COMPANIES FOUND (From CSV - 1 result(s)):
   Search criteria: is , 547, dr rajendra prasad rd...
   Matching rows:

   Row 26:
      Company: DIX IT STORE
      Address: 547, Dr Rajendra Prasad Rd, opposite to RISHABA POLY PACKS, Coimbatore, Tamil Nadu
      Phone: nan
      Website: nan

Your question: tell about IT Konnect

📋 COMPANY DETAILS (From CSV - Row 3):
   Title: IT Konnect
   totalScore: 4.9
   reviewsCount: 561.0
   street: 74, 100 Feet Rd
   city: Gandhipuram, Coimbatore
   state: Tamil Nadu
   website: https://itkonnect.in/
   phone: +91 74185 60077
   ...

Your question: exit
👋 Exiting agent...
```

---

## 🔐 Control Rules Verified

✅ **RULE 1** - Answers from CSV + Row references
```
Output: "Row 26: DIX IT STORE"
```

✅ **RULE 2** - Internet blocked
```
If online data needed:
"⚠️ INFORMATION NOT FOUND IN LOCAL DATASET
Do you permit online search? (Type 'Yes, search online')"
```

✅ **RULE 3** - Permission mode
```
Only accepts: "Yes, search online" or "You may use internet"
```

✅ **RULE 4** - Transparent reasoning
```
Shows: Row number, CSV columns, search criteria, all data used
```

✅ **RULE 5** - No fabrication  
```
Reports: "Data not found" - Never guesses
```

---

## 📞 Summary

Your **Controlled Data Assistant** is now:
- ✅ Answering your exact question correctly
- ✅ Logging every step with timestamps
- ✅ Following all 5 control rules
- ✅ Ready for production use

**Start with:**
```bash
python csv_reader.py
```

**Check logs:**
```bash
tail agent.log
```

Enjoy! 🚀
