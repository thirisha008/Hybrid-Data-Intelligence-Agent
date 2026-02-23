# import pandas as pd
# import ollama
# import logging
# import re
# import traceback
# from ddgs import DDGS

# MODEL_NAME = "qwen3-vl:4b"

# # -------- LOGGING ----------
# logging.basicConfig(
#     filename="agent.log",
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s"
# )

# class CSVAgent:
#     def __init__(self):
#         self.df = None

#     # -------- LOAD CSV ----------
#     def load_csv(self):
#         try:
#             path = input("Enter CSV file path: ")
#             self.df = pd.read_csv(path)

#             print("\n✅ CSV Loaded Successfully!")
#             print("Columns:", list(self.df.columns))

#             logging.info(f"CSV loaded: {path}")

#         except Exception as e:
#             logging.error(traceback.format_exc())
#             print("Error loading CSV:", e)

#     # -------- WEB SEARCH ----------
#     def web_search(self, query):
#         print("\n🌐 Performing Web Search...\n")
#         logging.info(f"Web search: {query}")

#         try:
#             with DDGS() as ddgs:
#                 results = list(ddgs.text(query, max_results=3))

#             if not results:
#                 print("No results found.")
#                 return

#             for r in results:
#                 print("Title   :", r["title"])
#                 print("Link    :", r["href"])
#                 print("Snippet :", r["body"])
#                 print("-" * 50)

#         except Exception:
#             logging.error(traceback.format_exc())
#             print("Web search failed.")

#     # -------- LLM NORMAL RESPONSE ----------
#     def llm_chat(self, question):
#         print("\n🤖 Thinking...\n")
#         logging.info(f"LLM question: {question}")

#         try:
#             response = ollama.chat(
#                 model=MODEL_NAME,
#                 messages=[
#                     {
#                         "role": "system",
#                         "content": "You are a helpful assistant. Answer in 3-5 lines only. Keep it simple."
#                     },
#                     {
#                         "role": "user",
#                         "content": question
#                     }
#                 ],
#                 options={"temperature": 0.7}
#             )

#             answer = response.get("message", {}).get("content", "")

#             print("🤖 LLM Answer:\n")
#             print(answer)

#             logging.info(f"LLM answer: {answer}")

#         except Exception:
#             logging.error(traceback.format_exc())
#             print("LLM failed.")

#     # -------- ADDRESS HANDLER ----------
#     def handle_address_query(self, question):
#         try:
#             q = question.lower()

#             if "address" in q or "location" in q:

#                 name = re.sub(r"give.*address of", "", q)
#                 name = re.sub(r"address of", "", name).strip()

#                 if "title" not in self.df.columns:
#                     return False

#                 match = self.df[self.df['title'].astype(str).str.lower().str.contains(name, na=False)]

#                 if not match.empty:
#                     row = match.iloc[0]

#                     address = f"{row.get('street','')}, {row.get('city','')}, {row.get('state','')}, {row.get('countryCode','')}"

#                     print("\n📍 Address Found:\n")
#                     print("Name    :", row.get('title', 'N/A'))
#                     print("Address :", address)
#                     print("Phone   :", row.get('phone', 'N/A'))
#                     print("Website :", row.get('website', 'N/A'))
#                     print("-" * 50)

#                     logging.info(f"Address found for: {row.get('title')}")

#                     return True

#         except Exception:
#             logging.error(traceback.format_exc())

#         return False

#     # -------- DATA QUESTION HANDLER ----------
#     def handle_data_query(self, question):
#         try:
#             q = question.lower()

#             # Normalize column names
#             columns = {col.lower(): col for col in self.df.columns}

#             # Match column intelligently
#             def match_column():
#                 for col in columns:
#                     words = col.replace("(", "").replace(")", "").split()
#                     if all(word in q for word in words):
#                         return columns[col]

#                 # fallback: partial match
#                 for col in columns:
#                     if any(word in col for word in q.split()):
#                         return columns[col]

#                 return None

#             col = match_column()

#             # --- AVG ---
#             if "average" in q or "avg" in q or "mean" in q:
#                 if col:
#                     value = pd.to_numeric(self.df[col], errors='coerce').mean()
#                     print("\n📊 Result:\n")
#                     print(f"Average of '{col}' = {value:.2f}")
#                     return True

#             # --- SUM ---
#             if "sum" in q or "total" in q:
#                 if col:
#                     value = pd.to_numeric(self.df[col], errors='coerce').sum()
#                     print("\n📊 Result:\n")
#                     print(f"Total of '{col}' = {value:.2f}")
#                     return True

#             # --- COUNT ---
#             if "count" in q:
#                 print("\n📊 Result:\n")
#                 print(f"Total rows = {len(self.df)}")
#                 return True

#             # --- MAX ---
#             if "max" in q:
#                 if col:
#                     value = pd.to_numeric(self.df[col], errors='coerce').max()
#                     print("\n📊 Result:\n")
#                     print(f"Max of '{col}' = {value}")
#                     return True

#             # --- MIN ---
#             if "min" in q:
#                 if col:
#                     value = pd.to_numeric(self.df[col], errors='coerce').min()
#                     print("\n📊 Result:\n")
#                     print(f"Min of '{col}' = {value}")
#                     return True

#         except Exception:
#             logging.error(traceback.format_exc())

#         return False

#     # -------- GENERAL QUESTION CHECK ----------
#     def is_general_question(self, question):
#         keywords = ["what", "why", "how", "explain", "define"]
#         return any(word in question.lower() for word in keywords)

#     # -------- MAIN LOOP ----------
#     def ask(self):
#         while True:
#             question = input("\nAsk your question (type exit to quit): ")

#             if question.lower() == "exit":
#                 print("👋 Exiting agent...")
#                 break

#             logging.info(f"User: {question}")

#             # 1️⃣ Address
#             if self.handle_address_query(question):
#                 continue

#             # 2️⃣ Data query ✅ (FIXED)
#             if self.handle_data_query(question):
#                 continue

#             # 3️⃣ General → LLM
#             if self.is_general_question(question):
#                 self.llm_chat(question)
#                 continue

#             # 4️⃣ Fallback → Web
#             self.web_search(question)


# # -------- RUN ----------
# if __name__ == "__main__":
#     agent = CSVAgent()
#     agent.load_csv()
#     agent.ask()




import pandas as pd
import logging
import traceback
from ddgs import DDGS
import json

# -------- LOGGING CONFIGURATION ----------
logging.basicConfig(
    filename="agent.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - [%(funcName)s] - %(message)s"
)

class ControlledDataAssistant:
    """
    RULE 1 — PRIMARY DATA SOURCE: Strictly read and answer from CSV only
    RULE 2 — NO INTERNET: No online sources unless explicitly permitted
    RULE 3 — ONLINE PERMISSION: Only allowed if user says "Yes, search online" or "You may use internet"
    RULE 4 — EXPLANATION MODE: Always show which rows/columns were used
    RULE 5 — NO FABRICATION: Never guess, infer, or use prior knowledge
    """

    def __init__(self):
        self.df = None
        self.csv_path = None
        self.online_permitted = False
        logging.info("ControlledDataAssistant initialized")

    # -------- LOAD CSV ----------
    def load_csv(self):
        """Load any CSV file"""
        try:
            path = input("Enter CSV file path: ").strip()
            self.df = pd.read_csv(path)
            self.csv_path = path

            logging.info(f"CSV loaded successfully: {path}")
            logging.info(f"Dataset shape: {len(self.df)} rows, {len(self.df.columns)} columns")
            logging.info(f"Columns: {', '.join(self.df.columns.tolist())}")

            print("\n✅ CSV Loaded Successfully!")
            print(f"📄 File: {path}")
            print(f"📊 Rows: {len(self.df)}, Columns: {len(self.df.columns)}")
            print(f"📋 Columns: {', '.join(self.df.columns.tolist())}\n")

        except FileNotFoundError:
            logging.error(f"File not found: {path}")
            print("❌ File not found.")
        except Exception as e:
            logging.error(f"Error loading CSV: {traceback.format_exc()}")
            print(f"❌ Error loading CSV: {e}")

    # -------- GET CSV METADATA ----------
    def get_csv_metadata(self):
        """Get metadata about the CSV for LLM code generation"""
        try:
            metadata = {
                "total_rows": len(self.df),
                "total_columns": len(self.df.columns),
                "columns": self.df.columns.tolist(),
                "column_dtypes": {col: str(dtype) for col, dtype in self.df.dtypes.items()},
                "sample_rows": self.df.head(2).to_dict('records')
            }
            
            logging.debug(f"CSV Metadata extracted: {len(self.df.columns)} columns, {len(self.df)} rows")
            logging.debug(f"Column names: {metadata['columns']}")
            logging.debug(f"Sample data: {metadata['sample_rows']}")
            
            return metadata
        except Exception as e:
            logging.error(f"Error getting CSV metadata: {traceback.format_exc()}")
            return None

    # -------- SEARCH CSV BY PARTIAL MATCH ----------
    def search_csv_smart(self, search_terms):
        """Search CSV for rows matching search terms across all columns"""
        logging.info(f"Starting smart search for: {search_terms}")
        
        try:
            # Split search terms
            terms = [t.strip().lower() for t in search_terms.split(',')]
            
            logging.debug(f"Search terms: {terms}")
            
            # Find rows that match ALL terms
            mask = pd.Series([True] * len(self.df))
            
            for term in terms:
                if term:
                    # Create a mask for this term across all columns
                    term_mask = pd.Series([False] * len(self.df))
                    for col in self.df.columns:
                        col_lower = self.df[col].astype(str).str.lower()
                        col_term_mask = col_lower.str.contains(term, na=False)
                        term_mask = term_mask | col_term_mask
                    
                    mask = mask & term_mask
                    logging.debug(f"After filtering for '{term}': {mask.sum()} rows remaining")
            
            matching_rows = self.df[mask]
            logging.info(f"Search returned {len(matching_rows)} matching rows")
            
            return matching_rows
        except Exception as e:
            logging.error(f"Error in smart search: {traceback.format_exc()}")
            return pd.DataFrame()

    # -------- SEARCH BY ADDRESS ----------
    def search_by_address(self, question):
        """Search for companies by address"""
        logging.info(f"Address search initiated for: {question}")
        
        try:
            # Extract address keywords from question
            keywords = question.lower()
            
            # Remove common phrases
            keywords = keywords.replace("which company", "").replace("located", "").replace("in", ",").replace("at", ",")
            keywords = keywords.replace("?", "").strip()
            
            # Remove extra quotes and special characters that might have been pasted
            keywords = keywords.replace('"', "").replace("'", "").replace("``", "").replace("'", "")
            
            # Clean up spacing
            keywords = " ".join(keywords.split())
            
            logging.debug(f"Extracted keywords: {keywords}")
            
            # Search across all columns for address keywords
            matches = self.search_csv_smart(keywords)
            
            if not matches.empty:
                logging.info(f"Found {len(matches)} companies matching address criteria")
                print(f"\n📍 COMPANIES FOUND (From CSV - {len(matches)} result(s)):")
                print(f"   Search criteria: {keywords}")
                print(f"   Matching rows:\n")
                
                for idx, row in matches.iterrows():
                    print(f"   Row {idx + 1}:")
                    print(f"      Company: {row.get('title', 'N/A')}")
                    print(f"      Address: {row.get('street', 'N/A')}, {row.get('city', 'N/A')}, {row.get('state', 'N/A')}")
                    print(f"      Phone: {row.get('phone', 'N/A')}")
                    print(f"      Website: {row.get('website', 'N/A')}")
                    print()
                
                logging.info(f"Address search successful, returned {len(matches)} results")
                return True
            else:
                logging.warning(f"No matches found for address search: {keywords}")
                return False
        except Exception as e:
            logging.error(f"Error in address search: {traceback.format_exc()}")
            return False

    # -------- FIND BEST MATCHING COLUMN ----------
    def find_column(self, keyword):
        """Find column that best matches keyword"""
        if not keyword:
            return None

        cols = self.df.columns.tolist()
        keyword_lower = keyword.lower()

        # Exact match (case-insensitive)
        for col in cols:
            if col.lower() == keyword_lower:
                logging.debug(f"Exact column match found: {col}")
                return col

        # Partial match - word in column name
        for col in cols:
            if keyword_lower in col.lower():
                logging.debug(f"Partial column match found: {col}")
                return col

        # Fuzzy: all words in keyword appear in column
        for col in cols:
            col_words = col.lower().replace("(", "").replace(")", "").split()
            keyword_words = keyword_lower.split()
            if all(word in col_words for word in keyword_words):
                logging.debug(f"Fuzzy column match found: {col}")
                return col

        logging.warning(f"No column match found for keyword: {keyword}")
        return None

    # -------- ANSWER DATA QUESTIONS ----------
    def answer_data_question(self, question):
        """Answer aggregation questions (count, sum, avg, max, min, etc.)"""
        q = question.lower()
        logging.info(f"Processing data aggregation question: {question}")
        
        # COUNT total rows
        if (("count" in q) or ("how many" in q)) and ("rows" in q or "entries" in q):
            result = len(self.df)
            logging.info(f"Row count result: {result}")
            print(f"\n📊 ANSWER (From CSV):")
            print(f"   Total rows in dataset: {result}")
            print(f"   Source: All {result} rows in '{self.csv_path}'")
            return True

        # COUNT specific column values
        if "count" in q and "how many" in q:
            keywords = q.replace("count", "").replace("how many", "").replace("?", "").strip()
            col = self.find_column(keywords)

            if col:
                count = self.df[col].notna().sum()
                logging.info(f"Count for column '{col}': {count} non-null values")
                print(f"\n📊 ANSWER (From CSV):")
                print(f"   Column: '{col}'")
                print(f"   Non-null values: {count}")
                print(f"   Source: Counted rows 1-{len(self.df)} in column '{col}'")
                return True

        # AVERAGE / MEAN
        if any(word in q for word in ["average", "mean", "avg"]):
            col_keyword = q.replace("average", "").replace("mean", "").replace("avg", "").replace("?", "").strip()
            col = self.find_column(col_keyword)

            if col:
                try:
                    numeric_col = pd.to_numeric(self.df[col], errors='coerce')
                    valid_count = numeric_col.notna().sum()
                    avg_value = numeric_col.mean()
                    
                    logging.info(f"Average calculation for '{col}': {avg_value} (from {valid_count} valid values)")
                    print(f"\n📊 ANSWER (From CSV):")
                    print(f"   Column: '{col}'")
                    print(f"   Average: {avg_value:.2f}")
                    print(f"   Sample values: {numeric_col.dropna().head(3).tolist()}")
                    print(f"   Source: Calculated from {valid_count} valid rows out of {len(self.df)}")
                    return True
                except Exception as e:
                    logging.error(f"Error calculating average: {e}")

        # SUM / TOTAL
        if any(word in q for word in ["sum", "total"]):
            col_keyword = q.replace("sum", "").replace("total", "").replace("?", "").strip()
            col = self.find_column(col_keyword)

            if col:
                try:
                    numeric_col = pd.to_numeric(self.df[col], errors='coerce')
                    valid_count = numeric_col.notna().sum()
                    sum_value = numeric_col.sum()
                    
                    logging.info(f"Sum calculation for '{col}': {sum_value}")
                    print(f"\n📊 ANSWER (From CSV):")
                    print(f"   Column: '{col}'")
                    print(f"   Sum: {sum_value:.2f}")
                    print(f"   Valid entries: {valid_count} out of {len(self.df)}")
                    print(f"   Source: Summed rows 1-{len(self.df)} in column '{col}'")
                    return True
                except Exception as e:
                    logging.error(f"Error calculating sum: {e}")

        # MAX
        if "max" in q or "maximum" in q:
            col_keyword = q.replace("max", "").replace("maximum", "").replace("?", "").strip()
            col = self.find_column(col_keyword)

            if col:
                try:
                    numeric_col = pd.to_numeric(self.df[col], errors='coerce')
                    max_value = numeric_col.max()
                    max_row_idx = numeric_col.idxmax()
                    
                    logging.info(f"Max value for '{col}': {max_value} at row {max_row_idx + 1}")
                    print(f"\n📊 ANSWER (From CSV):")
                    print(f"   Column: '{col}'")
                    print(f"   Maximum value: {max_value}")
                    print(f"   Found in row: {max_row_idx + 1}")
                    print(f"   Source: Scanned {len(self.df)} rows")
                    return True
                except Exception as e:
                    logging.error(f"Error calculating max: {e}")

        # MIN
        if "min" in q or "minimum" in q:
            col_keyword = q.replace("min", "").replace("minimum", "").replace("?", "").strip()
            col = self.find_column(col_keyword)

            if col:
                try:
                    numeric_col = pd.to_numeric(self.df[col], errors='coerce')
                    min_value = numeric_col.min()
                    min_row_idx = numeric_col.idxmin()
                    
                    logging.info(f"Min value for '{col}': {min_value} at row {min_row_idx + 1}")
                    print(f"\n📊 ANSWER (From CSV):")
                    print(f"   Column: '{col}'")
                    print(f"   Minimum value: {min_value}")
                    print(f"   Found in row: {min_row_idx + 1}")
                    print(f"   Source: Scanned {len(self.df)} rows")
                    return True
                except Exception as e:
                    logging.error(f"Error calculating min: {e}")

        logging.warning(f"Could not answer data question: {question}")
        return False

    # -------- EXTRACT COMPANY NAME ----------
    def extract_company_name(self, question):
        """Extract company name from question"""
        q = question.lower()
        
        phrases_to_remove = [
            "tell me about", "tell about", "what about", "info on", "details on",
            "give me", "give the", "what is the", "what is", "find", "show", "which",
            "company", "the", "of the", "for the", "of "
        ]
        
        for phrase in phrases_to_remove:
            q = q.replace(phrase, " ").strip()
        
        metrics = ["reviewcount", "review count", "reviews", "phone", "address", 
                   "street", "website", "score", "rating", "category"]
        for metric in metrics:
            q = q.replace(metric, " ").strip()
        
        q = q.replace("?", "").replace("'s", "").strip()
        q = " ".join(q.split())
        
        logging.debug(f"Extracted company name: {q}")
        return q.strip()

    # -------- SEARCH FOR COMPANY BY NAME ----------
    def search_company(self, company_name):
        """Search for company by name"""
        logging.info(f"Searching for company: {company_name}")
        
        if 'title' not in self.df.columns or not company_name:
            logging.warning(f"Cannot search company - title column missing or empty name")
            return None
        
        company_lower = company_name.lower().strip()
        
        # Exact match first
        matches = self.df[
            self.df['title'].astype(str).str.lower() == company_lower
        ]
        
        if not matches.empty:
            logging.info(f"Exact match found: {matches.iloc[0]['title']} at row {matches.index[0] + 1}")
            return matches.iloc[0], matches.index[0]
        
        # Partial match
        matches = self.df[
            self.df['title'].astype(str).str.lower().str.contains(company_lower, na=False)
        ]
        
        if not matches.empty:
            logging.info(f"Partial match found: {matches.iloc[0]['title']} at row {matches.index[0] + 1}")
            return matches.iloc[0], matches.index[0]
        
        logging.warning(f"No company found matching: {company_name}")
        return None

    # -------- EXTRACT METRIC NAME ----------
    def extract_metric(self, question):
        """Extract requested metric from question"""
        q = question.lower()
        logging.debug(f"Extracting metric from: {question}")
        
        if "reviewcount" in q or "review count" in q or "reviews" in q:
            logging.debug("Metric identified: reviewsCount")
            return "reviewsCount"
        elif "score" in q and "total" in q:
            logging.debug("Metric identified: totalScore")
            return "totalScore"
        elif "score" in q or "rating" in q:
            logging.debug("Metric identified: totalScore")
            return "totalScore"
        elif "phone" in q or "contact" in q or "call" in q:
            logging.debug("Metric identified: phone")
            return "phone"
        elif "address" in q or "location" in q or "street" in q or "where" in q:
            logging.debug("Metric identified: address (multiple columns)")
            return ["street", "city", "state", "countryCode"]
        elif "website" in q or "url" in q or "web" in q:
            logging.debug("Metric identified: website")
            return "website"
        elif "category" in q or "categories" in q or "type" in q:
            logging.debug("Metric identified: categoryName")
            return "categoryName"
        
        logging.debug("No specific metric identified")
        return None

    # -------- ANSWER COMPANY SPECIFIC QUESTION ----------
    def answer_company_question(self, question):
        """Answer questions about specific companies"""
        q = question.lower()
        logging.info(f"Processing company question: {question}")
        
        company_keywords = ["tell", "about", "info", "details", "what is", "phone", 
                           "address", "website", "review", "score", "rating", "category",
                           "the", "of"]
        
        if any(keyword in q for keyword in company_keywords):
            
            company_name = self.extract_company_name(question)
            
            if company_name and len(company_name) > 1:
                result = self.search_company(company_name)
                
                if result:
                    row, row_idx = result
                    logging.info(f"Company found: {row['title']} at row {row_idx + 1}")
                    
                    metric = self.extract_metric(question)
                    
                    if metric:
                        if isinstance(metric, list):
                            print(f"\n📍 ANSWER (From CSV - Row {row_idx + 1}):")
                            print(f"   Company: '{row['title']}'")
                            for m in metric:
                                if m in row.index:
                                    value = row[m]
                                    if pd.notna(value) and value != 'nan':
                                        print(f"   {m}: {value}")
                                        logging.debug(f"Address detail - {m}: {value}")
                        else:
                            if metric in row.index:
                                value = row[metric]
                                if pd.notna(value) and value != 'nan':
                                    logging.info(f"Company metric answer - {metric}: {value}")
                                    print(f"\n📊 ANSWER (From CSV - Row {row_idx + 1}):")
                                    print(f"   Company: '{row['title']}'")
                                    print(f"   {metric}: {value}")
                                    return True
                    else:
                        print(f"\n📋 COMPANY DETAILS (From CSV - Row {row_idx + 1}):")
                        print(f"   Title: {row['title']}")
                        for col in self.df.columns:
                            if col != 'title':
                                value = row[col]
                                if pd.notna(value) and value != 'nan' and str(value) != 'nan':
                                    print(f"   {col}: {value}")
                        logging.info(f"Full company details returned for: {row['title']}")
                    
                    return True
        
        logging.debug("Not identified as company question")
        return False

    # -------- REQUEST ONLINE PERMISSION ----------
    def ask_online_permission(self, question):
        """Ask user for permission to search online"""
        logging.info(f"Information not found in CSV, requesting online permission for: {question}")
        
        print(f"\n⚠️  INFORMATION NOT FOUND IN LOCAL DATASET")
        print(f"Question: '{question}'")
        print(f"Available columns: {', '.join(self.df.columns.tolist())}\n")

        permission = input("Do you permit online search? (Type 'Yes, search online' or 'You may use internet'): ").strip().lower()
        logging.info(f"Online permission response: {permission}")

        if permission in ["yes, search online", "you may use internet", "yes"]:
            self.online_permitted = True
            logging.info("Online search permitted by user")
            return True
        else:
            logging.info("Online search denied by user")
            print("❌ Online search denied. Staying restricted to CSV only.\n")
            return False

    # -------- WEB SEARCH ----------
    def web_search(self, query):
        """Perform web search if permitted"""
        if not self.online_permitted:
            logging.warning("Web search attempted but not permitted")
            return False

        logging.info(f"Performing web search for: {query}")
        print(f"\n🌐 Searching online for: '{query}'\n")

        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=3))

            if not results:
                logging.info("Web search returned no results")
                print("No online results found.")
                return False

            logging.info(f"Web search returned {len(results)} results")
            print("🌐 ONLINE SEARCH RESULTS:\n")
            for i, r in enumerate(results, 1):
                print(f"   [{i}] {r.get('title', 'N/A')}")
                print(f"       Link: {r.get('href', 'N/A')}")
                print(f"       Summary: {r.get('body', 'N/A')[:100]}...\n")

            return True

        except Exception:
            logging.error(f"Web search error: {traceback.format_exc()}")
            print("❌ Web search failed.\n")
            return False

    # -------- IS DATA QUESTION ----------
    def is_data_question(self, question):
        """Check if question is about CSV data aggregation"""
        keywords = ["count", "sum", "total", "average", "mean", "max", "min", 
                   "how many", "rows", "entries"]
        is_data_q = any(word in question.lower() for word in keywords)
        logging.debug(f"Data question check: {is_data_q}")
        return is_data_q

    # -------- IS ADDRESS QUESTION ----------
    def is_address_question(self, question):
        """Check if question is about location/address"""
        keywords = ["located", "location", "address", "road", "rd", "street", "st", "avenue", "ave"]
        is_addr_q = any(word in question.lower() for word in keywords)
        logging.debug(f"Address question check: {is_addr_q}")
        return is_addr_q

    # -------- MAIN INTERACTION LOOP ----------
    def interact(self):
        """Main conversation loop"""
        logging.info("Starting interaction loop")
        
        print("\n" + "="*60)
        print("🤖 CONTROLLED DATA ASSISTANT (CSV-ONLY MODE)")
        print("="*60)
        print("RULES:")
        print("  • All answers come STRICTLY from CSV")
        print("  • No assumptions or prior knowledge")
        print("  • Reasoning shown with row/column references")
        print("  • Online search requires your permission")
        print("  • Type 'exit' to quit\n")

        while True:
            question = input("Your question: ").strip()

            if question.lower() == "exit":
                logging.info("User exited the assistant")
                print("👋 Exiting agent...\n")
                break

            if not question:
                logging.debug("Empty question received")
                print("⚠️  Please enter a question.\n")
                continue

            logging.info(f"Processing user question: {question}")

            # 1️⃣ Check for address questions first
            if self.is_address_question(question):
                logging.debug("Identified as address question")
                if self.search_by_address(question):
                    print()
                    continue

            # 2️⃣ Try company-specific questions
            if self.answer_company_question(question):
                logging.debug("Successfully answered as company question")
                print()
                continue

            # 3️⃣ Try data aggregation questions
            if self.is_data_question(question):
                logging.debug("Identified as data question")
                if self.answer_data_question(question):
                    print()
                    continue

            # 4️⃣ Data not found - ask for online permission
            logging.warning(f"Could not answer from CSV: {question}")
            if self.ask_online_permission(question):
                self.web_search(question)
            
            print()


# -------- RUN ----------
if __name__ == "__main__":
    logging.info("="*70)
    logging.info("CONTROLLED DATA ASSISTANT STARTED")
    logging.info("="*70)
    
    assistant = ControlledDataAssistant()
    assistant.load_csv()
    
    if assistant.df is not None:
        assistant.interact()
    else:
        logging.error("Failed to load CSV, exiting")
        print("❌ Failed to load CSV. Exiting.")
    
    logging.info("="*70)
    logging.info("CONTROLLED DATA ASSISTANT ENDED")
    logging.info("="*70)
    """
    RULE 1 — PRIMARY DATA SOURCE: Strictly read and answer from CSV only
    RULE 2 — NO INTERNET: No online sources unless explicitly permitted
    RULE 3 — ONLINE PERMISSION: Only allowed if user says "Yes, search online" or "You may use internet"
    RULE 4 — EXPLANATION MODE: Always show which rows/columns were used
    RULE 5 — NO FABRICATION: Never guess, infer, or use prior knowledge
    """

    def __init__(self):
        self.df = None
        self.csv_path = None
        self.online_permitted = False

    # -------- LOAD CSV ----------
    def load_csv(self):
        """Load any CSV file"""
        try:
            path = input("Enter CSV file path: ").strip()
            self.df = pd.read_csv(path)
            self.csv_path = path

            print("\n✅ CSV Loaded Successfully!")
            print(f"📄 File: {path}")
            print(f"📊 Rows: {len(self.df)}, Columns: {len(self.df.columns)}")
            print(f"📋 Columns: {', '.join(self.df.columns.tolist())}\n")

            logging.info(f"CSV loaded: {path}")

        except FileNotFoundError:
            print("❌ File not found.")
        except Exception as e:
            logging.error(traceback.format_exc())
            print(f"❌ Error loading CSV: {e}")

    # -------- FIND BEST MATCHING COLUMN ----------
    def find_column(self, keyword):
        """Find column that best matches keyword"""
        if not keyword:
            return None

        cols = self.df.columns.tolist()
        keyword_lower = keyword.lower()

        # Exact match (case-insensitive)
        for col in cols:
            if col.lower() == keyword_lower:
                return col

        # Partial match - word in column name
        for col in cols:
            if keyword_lower in col.lower():
                return col

        # Fuzzy: all words in keyword appear in column
        for col in cols:
            col_words = col.lower().replace("(", "").replace(")", "").split()
            keyword_words = keyword_lower.split()
            if all(word in col_words for word in keyword_words):
                return col

        return None

    # -------- ANSWER DATA QUESTIONS ----------
    def answer_data_question(self, question):
        """Answer aggregation questions (count, sum, avg, max, min, etc.)"""
        q = question.lower()
        
        # COUNT total rows
        if (("count" in q) or ("how many" in q)) and ("rows" in q or "entries" in q):
            result = len(self.df)
            print(f"\n📊 ANSWER (From CSV):")
            print(f"   Total rows in dataset: {result}")
            print(f"   Source: All {result} rows in '{self.csv_path}'")
            logging.info(f"Answer: Total rows = {result}")
            return True

        # COUNT specific column values
        if "count" in q and "how many" in q:
            # Extract column name from question
            keywords = q.replace("count", "").replace("how many", "").replace("?", "").strip()
            col = self.find_column(keywords)

            if col:
                count = self.df[col].notna().sum()
                print(f"\n📊 ANSWER (From CSV):")
                print(f"   Column: '{col}'")
                print(f"   Non-null values: {count}")
                print(f"   Source: Counted rows 1-{len(self.df)} in column '{col}'")
                logging.info(f"Count answer: {col} = {count}")
                return True

        # AVERAGE / MEAN
        if any(word in q for word in ["average", "mean", "avg"]):
            col_keyword = q.replace("average", "").replace("mean", "").replace("avg", "").replace("?", "").strip()
            col = self.find_column(col_keyword)

            if col:
                try:
                    numeric_col = pd.to_numeric(self.df[col], errors='coerce')
                    valid_count = numeric_col.notna().sum()
                    avg_value = numeric_col.mean()
                    
                    print(f"\n📊 ANSWER (From CSV):")
                    print(f"   Column: '{col}'")
                    print(f"   Average: {avg_value:.2f}")
                    print(f"   Sample values: {numeric_col.dropna().head(3).tolist()}")
                    print(f"   Source: Calculated from {valid_count} valid rows out of {len(self.df)}")
                    logging.info(f"Average: {col} = {avg_value}")
                    return True
                except:
                    pass

        # SUM / TOTAL
        if any(word in q for word in ["sum", "total"]):
            col_keyword = q.replace("sum", "").replace("total", "").replace("?", "").strip()
            col = self.find_column(col_keyword)

            if col:
                try:
                    numeric_col = pd.to_numeric(self.df[col], errors='coerce')
                    valid_count = numeric_col.notna().sum()
                    sum_value = numeric_col.sum()
                    
                    print(f"\n📊 ANSWER (From CSV):")
                    print(f"   Column: '{col}'")
                    print(f"   Sum: {sum_value:.2f}")
                    print(f"   Valid entries: {valid_count} out of {len(self.df)}")
                    print(f"   Source: Summed rows 1-{len(self.df)} in column '{col}'")
                    logging.info(f"Sum: {col} = {sum_value}")
                    return True
                except:
                    pass

        # MAX
        if "max" in q or "maximum" in q:
            col_keyword = q.replace("max", "").replace("maximum", "").replace("?", "").strip()
            col = self.find_column(col_keyword)

            if col:
                try:
                    numeric_col = pd.to_numeric(self.df[col], errors='coerce')
                    max_value = numeric_col.max()
                    max_row_idx = numeric_col.idxmax()
                    
                    print(f"\n📊 ANSWER (From CSV):")
                    print(f"   Column: '{col}'")
                    print(f"   Maximum value: {max_value}")
                    print(f"   Found in row: {max_row_idx + 1}")
                    print(f"   Full row: {self.df.iloc[max_row_idx].to_dict()}")
                    print(f"   Source: Scanned {len(self.df)} rows")
                    logging.info(f"Max: {col} = {max_value} at row {max_row_idx}")
                    return True
                except:
                    pass

        # MIN
        if "min" in q or "minimum" in q:
            col_keyword = q.replace("min", "").replace("minimum", "").replace("?", "").strip()
            col = self.find_column(col_keyword)

            if col:
                try:
                    numeric_col = pd.to_numeric(self.df[col], errors='coerce')
                    min_value = numeric_col.min()
                    min_row_idx = numeric_col.idxmin()
                    
                    print(f"\n📊 ANSWER (From CSV):")
                    print(f"   Column: '{col}'")
                    print(f"   Minimum value: {min_value}")
                    print(f"   Found in row: {min_row_idx + 1}")
                    print(f"   Full row: {self.df.iloc[min_row_idx].to_dict()}")
                    print(f"   Source: Scanned {len(self.df)} rows")
                    logging.info(f"Min: {col} = {min_value} at row {min_row_idx}")
                    return True
                except:
                    pass

        return False

    # -------- EXTRACT COMPANY NAME ----------
    def extract_company_name(self, question):
        """Extract company name from question more intelligently"""
        q = question.lower()
        
        # Remove common metric keywords and phrases first
        phrases_to_remove = [
            "tell me about", "tell about", "what about", "info on", "details on",
            "give me", "give the", "what is the", "what is", "find", "show", "which",
            "company", "the", "of the", "for the", "of "
        ]
        
        for phrase in phrases_to_remove:
            q = q.replace(phrase, " ").strip()
        
        # Remove metric keywords
        metrics = ["reviewcount", "review count", "reviews", "phone", "address", 
                   "street", "website", "score", "rating", "category"]
        for metric in metrics:
            q = q.replace(metric, " ").strip()
        
        # Remove question marks and extra spaces
        q = q.replace("?", "").replace("'s", "").strip()
        
        # Clean up remaining whitespace
        q = " ".join(q.split())
        
        return q.strip()

    # -------- SEARCH FOR COMPANY BY NAME ----------
    def search_company(self, company_name):
        """Search for company by exact or partial name match"""
        if 'title' not in self.df.columns or not company_name:
            return None
        
        company_lower = company_name.lower().strip()
        
        # Exact match first
        matches = self.df[
            self.df['title'].astype(str).str.lower() == company_lower
        ]
        
        if not matches.empty:
            return matches.iloc[0], matches.index[0]
        
        # Partial match - company name appears in title
        matches = self.df[
            self.df['title'].astype(str).str.lower().str.contains(company_lower, na=False)
        ]
        
        if not matches.empty:
            return matches.iloc[0], matches.index[0]
        
        return None

    # -------- EXTRACT METRIC NAME ----------
    def extract_metric(self, question):
        """Extract what metric user is asking for"""
        q = question.lower()
        
        if "reviewcount" in q or "review count" in q or "reviews" in q:
            return "reviewsCount"
        elif "score" in q and "total" in q:
            return "totalScore"
        elif "score" in q or "rating" in q:
            return "totalScore"
        elif "phone" in q or "contact" in q or "call" in q:
            return "phone"
        elif "address" in q or "location" in q or "street" in q or "where" in q:
            return ["street", "city", "state", "countryCode"]
        elif "website" in q or "url" in q or "web" in q:
            return "website"
        elif "category" in q or "categories" in q or "type" in q:
            return "categoryName"
        
        return None

    # -------- ANSWER COMPANY SPECIFIC QUESTION ----------
    def answer_company_question(self, question):
        """Answer questions about specific companies"""
        q = question.lower()
        
        # Check if it's asking about a company
        company_keywords = ["tell", "about", "info", "details", "what is", "phone", 
                           "address", "website", "review", "score", "rating", "category",
                           "the", "of"]
        
        if any(keyword in q for keyword in company_keywords):
            
            company_name = self.extract_company_name(question)
            
            if company_name and len(company_name) > 1:  # Must be meaningful
                result = self.search_company(company_name)
                
                if result:
                    row, row_idx = result
                    
                    # Check if asking for specific metric
                    metric = self.extract_metric(question)
                    
                    if metric:
                        if isinstance(metric, list):
                            # Multiple columns (like address)
                            print(f"\n📍 ANSWER (From CSV - Row {row_idx + 1}):")
                            print(f"   Company: '{row['title']}'")
                            for m in metric:
                                if m in row.index:
                                    value = row[m]
                                    if pd.notna(value) and value != 'nan':
                                        print(f"   {m}: {value}")
                        else:
                            # Single metric
                            if metric in row.index:
                                value = row[metric]
                                if pd.notna(value) and value != 'nan':
                                    print(f"\n📊 ANSWER (From CSV - Row {row_idx + 1}):")
                                    print(f"   Company: '{row['title']}'")
                                    print(f"   {metric}: {value}")
                                    logging.info(f"Company metric: {company_name} - {metric} = {value}")
                                    return True
                    else:
                        # Return full company details
                        print(f"\n📋 COMPANY DETAILS (From CSV - Row {row_idx + 1}):")
                        print(f"   Title: {row['title']}")
                        for col in self.df.columns:
                            if col != 'title':
                                value = row[col]
                                if pd.notna(value) and value != 'nan' and str(value) != 'nan':
                                    print(f"   {col}: {value}")
                    
                    logging.info(f"Company search: {company_name} found at row {row_idx + 1}")
                    return True
        
        return False

    # -------- SEARCH CSV FOR ROWS ----------
    def search_csv(self, question):
        """Search for specific rows matching criteria"""
        q = question.lower()

        # Extract search term (everything after "find", "show", "which", "what")
        search_term = q.replace("find", "").replace("show", "").replace("which", "").replace("what", "").strip()
        
        # Try to match columns and values
        for col in self.df.columns:
            col_lower = col.lower()
            
            # Check if searching by column value
            if col_lower in search_term:
                value_to_search = search_term.replace(col_lower, "").strip()
                
                matches = self.df[
                    self.df[col].astype(str).str.lower().str.contains(value_to_search, na=False)
                ]
                
                if not matches.empty:
                    print(f"\n📋 SEARCH RESULTS (From CSV):")
                    print(f"   Column: '{col}'")
                    print(f"   Search term: '{value_to_search}'")
                    print(f"   Matches found: {len(matches)} rows\n")
                    
                    for idx, row in matches.iterrows():
                        print(f"   Row {idx + 1}:")
                        for col_name in self.df.columns:
                            print(f"      - {col_name}: {row[col_name]}")
                        print()
                    
                    logging.info(f"Search found {len(matches)} rows for '{value_to_search}' in '{col}'")
                    return True

        return False

    # -------- REQUEST ONLINE PERMISSION ----------
    def ask_online_permission(self, question):
        """Ask user for permission to search online"""
        print(f"\n⚠️  INFORMATION NOT FOUND IN LOCAL DATASET")
        print(f"Question: '{question}'")
        print(f"Available columns: {', '.join(self.df.columns.tolist())}\n")

        permission = input("Do you permit online search? (Type 'Yes, search online' or 'You may use internet'): ").strip().lower()

        if permission in ["yes, search online", "you may use internet", "yes"]:
            self.online_permitted = True
            return True
        else:
            print("❌ Online search denied. Staying restricted to CSV only.\n")
            return False

    # -------- WEB SEARCH ----------
    def web_search(self, query):
        """Perform web search if permitted"""
        if not self.online_permitted:
            return False

        print(f"\n🌐 Searching online for: '{query}'\n")
        logging.info(f"Web search: {query}")

        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=3))

            if not results:
                print("No online results found.")
                return False

            print("🌐 ONLINE SEARCH RESULTS:\n")
            for i, r in enumerate(results, 1):
                print(f"   [{i}] {r.get('title', 'N/A')}")
                print(f"       Link: {r.get('href', 'N/A')}")
                print(f"       Summary: {r.get('body', 'N/A')[:100]}...\n")

            logging.info(f"Web search returned {len(results)} results")
            return True

        except Exception:
            logging.error(traceback.format_exc())
            print("❌ Web search failed.\n")
            return False

    # -------- IS DATA QUESTION ----------
    def is_data_question(self, question):
        """Check if question is about CSV data aggregation"""
        keywords = ["count", "sum", "total", "average", "mean", "max", "min", 
                   "how many", "rows", "entries"]
        return any(word in question.lower() for word in keywords)

    # -------- MAIN INTERACTION LOOP ----------
    def interact(self):
        """Main conversation loop"""
        print("\n" + "="*60)
        print("🤖 CONTROLLED DATA ASSISTANT (CSV-ONLY MODE)")
        print("="*60)
        print("RULES:")
        print("  • All answers come STRICTLY from CSV")
        print("  • No assumptions or prior knowledge")
        print("  • Reasoning shown with row/column references")
        print("  • Online search requires your permission")
        print("  • Type 'exit' to quit\n")

        while True:
            question = input("Your question: ").strip()

            if question.lower() == "exit":
                print("👋 Exiting agent...\n")
                break

            if not question:
                print("⚠️  Please enter a question.\n")
                continue

            logging.info(f"User: {question}")

            # 1️⃣ Try company-specific questions first
            if self.answer_company_question(question):
                print()
                continue

            # 2️⃣ Try data aggregation questions
            if self.is_data_question(question):
                if self.answer_data_question(question):
                    print()
                    continue
                if self.search_csv(question):
                    print()
                    continue

            # 3️⃣ Data not found - ask for online permission
            if self.ask_online_permission(question):
                self.web_search(question)
            
            print()


# -------- RUN ----------
if __name__ == "__main__":
    assistant = ControlledDataAssistant()
    assistant.load_csv()
    if assistant.df is not None:
        assistant.interact()
    else:
        print("❌ Failed to load CSV. Exiting.")