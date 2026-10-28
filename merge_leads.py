import csv
import os
from pathlib import Path

LEADS_DIR = Path("Leads")
OUTPUT_FILE = "merged_leads.csv"
OUTPUT_DEDUP = "merged_leads_dedup.csv"

def get_all_csv_files(directory):
    return list(directory.glob("*.csv"))

def read_csv_files(files):
    rows = []
    header = None
    
    for file_path in files:
        with open(file_path, "r", encoding="utf-8-sig", errors="replace") as f:
            reader = csv.DictReader(f)
            if header is None:
                header = reader.fieldnames
            for row in reader:
                rows.append(row)
    
    return header, rows

def write_csv_file(file_path, header, rows):
    with open(file_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)

def dedupe_rows(rows):
    seen = set()
    deduped = []
    
    for row in rows:
        email = row.get("email", "").strip()
        full_name = row.get("full_name", "").strip()
        
        if email:
            key = email.lower()
        elif full_name:
            key = full_name.lower()
        else:
            key = None
        
        if key and key not in seen:
            seen.add(key)
            deduped.append(row)
        elif not key:
            deduped.append(row)
    
    return deduped

def main():
    csv_files = get_all_csv_files(LEADS_DIR)
    print(f"Found {len(csv_files)} CSV files")
    
    header, rows = read_csv_files(csv_files)
    print(f"Total rows: {len(rows)}")
    
    write_csv_file(OUTPUT_FILE, header, rows)
    print(f"Written: {OUTPUT_FILE}")
    
    deduped = dedupe_rows(rows)
    print(f"After dedupe: {len(deduped)}")
    
    write_csv_file(OUTPUT_DEDUP, header, deduped)
    print(f"Written: {OUTPUT_DEDUP}")
    
    print("Done!")

if __name__ == "__main__":
    main()